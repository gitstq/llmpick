"""核心引擎测试"""

import pytest

from llmpick.core import LLMPick
from llmpick.types import GPUInfo, GPUVendor, HardwareInfo, ModelInfo, QuantizationType


class TestLLMPick:
    """测试推荐引擎"""

    def test_engine_initialization(self):
        """测试引擎初始化"""
        picker = LLMPick()
        assert picker is not None
        assert picker.hardware_detector is not None
        assert picker.model_db is not None

    def test_recommend_returns_list(self):
        """测试推荐返回列表"""
        picker = LLMPick()
        
        # 创建测试硬件信息
        hardware = HardwareInfo(
            cpu_name="Test CPU",
            cpu_cores=8,
            ram_gb=16.0,
            disk_free_gb=100.0,
            gpus=[GPUInfo(name="RTX 4090", vendor=GPUVendor.NVIDIA, vram_gb=24.0)],
            has_cuda=True,
        )
        
        recommendations = picker.recommend(hardware=hardware, top_k=3)
        
        assert isinstance(recommendations, list)
        assert len(recommendations) <= 3

    def test_recommend_scores_ordered(self):
        """测试推荐分数排序"""
        picker = LLMPick()
        
        hardware = HardwareInfo(
            cpu_name="Test CPU",
            cpu_cores=8,
            ram_gb=16.0,
            disk_free_gb=100.0,
            gpus=[GPUInfo(name="RTX 4090", vendor=GPUVendor.NVIDIA, vram_gb=24.0)],
            has_cuda=True,
        )
        
        recommendations = picker.recommend(hardware=hardware, top_k=5)
        
        if len(recommendations) >= 2:
            scores = [r.score for r in recommendations]
            assert scores == sorted(scores, reverse=True)

    def test_calculate_score(self):
        """测试分数计算"""
        picker = LLMPick()
        
        model = ModelInfo(
            id="test-model",
            name="Test Model",
            repo_id="test/test",
            description="Test",
            parameters="7B",
            size_gb=4.0,
            quantization=QuantizationType.Q4_K_M,
            format="gguf",
            context_length=4096,
            benchmark_score=70.0,
        )
        
        hardware = HardwareInfo(
            cpu_name="Test CPU",
            cpu_cores=8,
            ram_gb=16.0,
            disk_free_gb=100.0,
            gpus=[GPUInfo(name="RTX 4090", vendor=GPUVendor.NVIDIA, vram_gb=24.0)],
        )
        
        rec = picker._calculate_score(model, hardware, 24.0)
        
        assert rec.model == model
        assert 0 <= rec.score <= 100
        assert rec.fit_type in ["perfect", "good", "partial", "tight", "cpu_only"]
        assert rec.estimated_tokens_per_sec > 0

    def test_get_model_download_command(self):
        """测试获取下载命令"""
        picker = LLMPick()
        
        model = ModelInfo(
            id="test-model",
            name="Test Model",
            repo_id="test/test-model-GGUF",
            description="Test",
            parameters="7B",
            size_gb=4.0,
            quantization=QuantizationType.Q4_K_M,
            format="gguf",
            context_length=4096,
        )
        
        cmd = picker.get_model_download_command(model, "ollama")
        assert "ollama" in cmd
        
        cmd = picker.get_model_download_command(model, "lmstudio")
        assert "LM Studio" in cmd

    def test_estimate_speed(self):
        """测试速度估算"""
        picker = LLMPick()
        
        model = ModelInfo(
            id="test-model",
            name="Test Model",
            repo_id="test/test",
            description="Test",
            parameters="7B",
            size_gb=4.0,
            quantization=QuantizationType.Q4_K_M,
            format="gguf",
            context_length=4096,
        )
        
        hardware = HardwareInfo(
            cpu_name="Test CPU",
            cpu_cores=8,
            ram_gb=16.0,
            disk_free_gb=100.0,
            gpus=[GPUInfo(name="RTX 4090", vendor=GPUVendor.NVIDIA, vram_gb=24.0)],
        )
        
        speed = picker._estimate_speed(model, hardware, "perfect")
        assert speed > 0
