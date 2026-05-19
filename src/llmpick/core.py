"""核心推荐引擎模块"""

from __future__ import annotations

import math
from typing import Optional

from llmpick.hardware import HardwareDetector
from llmpick.models import ModelDatabase
from llmpick.types import HardwareInfo, ModelInfo, Recommendation


class LLMPick:
    """LLM推荐引擎"""

    # 量化质量系数 (相对于Q4_K_M)
    QUANT_QUALITY = {
        "Q4_0": 0.90,
        "Q4_K_M": 1.00,
        "Q5_0": 0.95,
        "Q5_K_M": 1.05,
        "Q6_K": 1.08,
        "Q8_0": 1.10,
        "FP16": 1.15,
        "FP32": 1.20,
    }

    # 速度估算系数 (tokens/sec per GB/s memory bandwidth)
    SPEED_FACTOR = 0.5

    def __init__(self) -> None:
        """初始化推荐引擎"""
        self.hardware_detector = HardwareDetector()
        self.model_db = ModelDatabase()

    def recommend(
        self,
        hardware: Optional[HardwareInfo] = None,
        prefer_chinese: bool = True,
        top_k: int = 5,
    ) -> list[Recommendation]:
        """
        推荐适合的模型

        Args:
            hardware: 硬件信息，None则自动检测
            prefer_chinese: 是否优先中文模型
            top_k: 返回前k个推荐

        Returns:
            推荐列表
        """
        if hardware is None:
            hardware = self.hardware_detector.detect()

        # 获取可用显存
        available_vram = hardware.total_vram_gb if hardware.gpus else 0
        available_ram = hardware.ram_gb

        # 根据显存过滤模型
        if available_vram > 0:
            # 有GPU，按显存过滤
            candidates = self.model_db.filter_by_vram(available_vram)
        else:
            # 无GPU，按内存过滤（CPU推理）
            candidates = self.model_db.filter_by_vram(available_ram * 0.5)

        # 计算每个模型的推荐分数
        recommendations = []
        for model in candidates:
            rec = self._calculate_score(model, hardware, available_vram)
            recommendations.append(rec)

        # 排序：分数高的在前
        recommendations.sort(key=lambda x: x.score, reverse=True)

        # 如果优先中文，调整排序
        if prefer_chinese:
            recommendations.sort(
                key=lambda x: (x.model.is_chinese_optimized, x.score),
                reverse=True,
            )

        return recommendations[:top_k]

    def _calculate_score(
        self,
        model: ModelInfo,
        hardware: HardwareInfo,
        available_vram: float,
    ) -> Recommendation:
        """计算模型推荐分数"""
        # 基础分数来自benchmark
        base_score = model.benchmark_score or 50.0

        # 量化质量调整
        quant_quality = self.QUANT_QUALITY.get(model.quantization.value, 1.0)
        adjusted_score = base_score * quant_quality

        # 显存适配度
        if available_vram > 0:
            vram_ratio = model.size_gb / available_vram
            if vram_ratio <= 0.5:
                fit_type = "perfect"
                fit_multiplier = 1.0
            elif vram_ratio <= 0.7:
                fit_type = "good"
                fit_multiplier = 0.95
            elif vram_ratio <= 0.9:
                fit_type = "partial"
                fit_multiplier = 0.85
            else:
                fit_type = "tight"
                fit_multiplier = 0.75
            vram_usage = model.size_gb
        else:
            # CPU模式
            fit_type = "cpu_only"
            fit_multiplier = 0.60
            vram_usage = 0

        final_score = adjusted_score * fit_multiplier

        # 估算速度
        estimated_speed = self._estimate_speed(model, hardware, fit_type)

        # 生成推荐理由
        reason = self._generate_reason(model, fit_type, hardware)

        return Recommendation(
            model=model,
            score=round(final_score, 1),
            fit_type=fit_type,
            estimated_tokens_per_sec=round(estimated_speed, 1),
            vram_usage_gb=round(vram_usage, 1),
            reason=reason,
        )

    def _estimate_speed(
        self,
        model: ModelInfo,
        hardware: HardwareInfo,
        fit_type: str,
    ) -> float:
        """估算推理速度 (tokens/sec)"""
        if not hardware.gpus:
            # CPU模式
            return 5.0

        primary_gpu = hardware.primary_gpu
        if primary_gpu is None:
            return 5.0

        # 基于显存带宽估算
        # RTX 4090: ~1000 GB/s -> ~500 tokens/s (Q4)
        # 简化估算：假设每GB显存带宽约0.5 tokens/s
        vram_gb = primary_gpu.vram_gb

        # 根据模型大小和量化调整
        size_factor = 7.0 / max(float(model.parameters.replace("B", "")), 1.0)

        # 根据fit_type调整
        fit_factors = {
            "perfect": 1.0,
            "good": 0.85,
            "partial": 0.65,
            "tight": 0.45,
            "cpu_only": 0.1,
        }
        fit_factor = fit_factors.get(fit_type, 0.5)

        # 估算速度
        base_speed = vram_gb * 2  # 简化估算
        estimated = base_speed * size_factor * fit_factor

        return max(estimated, 1.0)

    def _generate_reason(
        self,
        model: ModelInfo,
        fit_type: str,
        hardware: HardwareInfo,
    ) -> str:
        """生成推荐理由"""
        reasons = []

        # 适配度说明
        fit_descriptions = {
            "perfect": "完美适配，显存充裕",
            "good": "良好适配，运行流畅",
            "partial": "部分适配，可能需要分层加载",
            "tight": "紧适配，性能可能受限",
            "cpu_only": "CPU运行，速度较慢",
        }
        reasons.append(fit_descriptions.get(fit_type, "未知适配状态"))

        # 特色说明
        if model.is_chinese_optimized:
            reasons.append("中文优化")
        if model.is_code_optimized:
            reasons.append("代码能力强")
        if model.is_multimodal:
            reasons.append("支持多模态")

        return "；".join(reasons)

    def get_model_download_command(self, model: ModelInfo, backend: str = "ollama") -> str:
        """获取模型下载命令"""
        if backend == "ollama":
            # 转换模型名称为ollama格式
            ollama_name = model.repo_id.split("/")[-1].lower().replace("-gguf", "")
            return f"ollama pull {ollama_name}"
        elif backend == "lmstudio":
            return f"# 在LM Studio中搜索: {model.repo_id}"
        elif backend == "llamacpp":
            filename = f"{model.name.lower().replace(' ', '-').replace('.', '')}.gguf"
            return f"wget https://huggingface.co/{model.repo_id}/resolve/main/{filename}"
        else:
            return f"# 请从 HuggingFace 下载: https://huggingface.co/{model.repo_id}"

    def get_model_run_command(self, model: ModelInfo, backend: str = "ollama") -> str:
        """获取模型运行命令"""
        if backend == "ollama":
            ollama_name = model.repo_id.split("/")[-1].lower().replace("-gguf", "")
            return f"ollama run {ollama_name}"
        elif backend == "lmstudio":
            return "# 在LM Studio中加载模型并开始对话"
        elif backend == "llamacpp":
            return f"./main -m {model.name.lower().replace(' ', '-').replace('.', '')}.gguf -i"
        else:
            return "# 请使用相应的推理框架运行模型"
