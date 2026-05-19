"""模型数据库模块"""

from __future__ import annotations

from llmpick.types import ModelFormat, ModelInfo, QuantizationType


class ModelDatabase:
    """模型数据库"""

    # 预设的模型数据
    MODELS: list[ModelInfo] = [
        # Qwen2.5 系列
        ModelInfo(
            id="qwen2.5-0.5b",
            name="Qwen2.5-0.5B",
            repo_id="Qwen/Qwen2.5-0.5B-Instruct-GGUF",
            description="通义千问2.5 0.5B指令模型，适合极低资源设备",
            parameters="0.5B",
            size_gb=0.4,
            quantization=QuantizationType.Q4_K_M,
            format=ModelFormat.GGUF,
            context_length=32768,
            is_chinese_optimized=True,
            tags=["qwen", "chinese", "instruct", "tiny"],
            benchmark_score=45.0,
        ),
        ModelInfo(
            id="qwen2.5-1.5b",
            name="Qwen2.5-1.5B",
            repo_id="Qwen/Qwen2.5-1.5B-Instruct-GGUF",
            description="通义千问2.5 1.5B指令模型，轻量高效",
            parameters="1.5B",
            size_gb=1.0,
            quantization=QuantizationType.Q4_K_M,
            format=ModelFormat.GGUF,
            context_length=32768,
            is_chinese_optimized=True,
            tags=["qwen", "chinese", "instruct", "small"],
            benchmark_score=55.0,
        ),
        ModelInfo(
            id="qwen2.5-3b",
            name="Qwen2.5-3B",
            repo_id="Qwen/Qwen2.5-3B-Instruct-GGUF",
            description="通义千问2.5 3B指令模型，性能与效率平衡",
            parameters="3B",
            size_gb=2.0,
            quantization=QuantizationType.Q4_K_M,
            format=ModelFormat.GGUF,
            context_length=32768,
            is_chinese_optimized=True,
            tags=["qwen", "chinese", "instruct", "medium"],
            benchmark_score=62.0,
        ),
        ModelInfo(
            id="qwen2.5-7b",
            name="Qwen2.5-7B",
            repo_id="Qwen/Qwen2.5-7B-Instruct-GGUF",
            description="通义千问2.5 7B指令模型，中文能力优秀",
            parameters="7B",
            size_gb=4.5,
            quantization=QuantizationType.Q4_K_M,
            format=ModelFormat.GGUF,
            context_length=32768,
            is_chinese_optimized=True,
            tags=["qwen", "chinese", "instruct", "large"],
            benchmark_score=70.0,
        ),
        ModelInfo(
            id="qwen2.5-14b",
            name="Qwen2.5-14B",
            repo_id="Qwen/Qwen2.5-14B-Instruct-GGUF",
            description="通义千问2.5 14B指令模型，更强推理能力",
            parameters="14B",
            size_gb=9.0,
            quantization=QuantizationType.Q4_K_M,
            format=ModelFormat.GGUF,
            context_length=32768,
            is_chinese_optimized=True,
            tags=["qwen", "chinese", "instruct", "xlarge"],
            benchmark_score=76.0,
        ),
        ModelInfo(
            id="qwen2.5-32b",
            name="Qwen2.5-32B",
            repo_id="Qwen/Qwen2.5-32B-Instruct-GGUF",
            description="通义千问2.5 32B指令模型，接近GPT-4水平",
            parameters="32B",
            size_gb=20.0,
            quantization=QuantizationType.Q4_K_M,
            format=ModelFormat.GGUF,
            context_length=32768,
            is_chinese_optimized=True,
            tags=["qwen", "chinese", "instruct", "xxlarge"],
            benchmark_score=82.0,
        ),
        # Llama 3 系列
        ModelInfo(
            id="llama-3.2-1b",
            name="Llama 3.2 1B",
            repo_id="bartowski/Llama-3.2-1B-Instruct-GGUF",
            description="Meta Llama 3.2 1B指令模型，边缘设备优化",
            parameters="1B",
            size_gb=0.7,
            quantization=QuantizationType.Q4_K_M,
            format=ModelFormat.GGUF,
            context_length=128000,
            tags=["llama", "meta", "instruct", "small", "multilingual"],
            benchmark_score=52.0,
        ),
        ModelInfo(
            id="llama-3.2-3b",
            name="Llama 3.2 3B",
            repo_id="bartowski/Llama-3.2-3B-Instruct-GGUF",
            description="Meta Llama 3.2 3B指令模型，视觉能力",
            parameters="3B",
            size_gb=2.0,
            quantization=QuantizationType.Q4_K_M,
            format=ModelFormat.GGUF,
            context_length=128000,
            is_multimodal=True,
            tags=["llama", "meta", "instruct", "medium", "vision", "multilingual"],
            benchmark_score=60.0,
        ),
        ModelInfo(
            id="llama-3.1-8b",
            name="Llama 3.1 8B",
            repo_id="bartowski/Meta-Llama-3.1-8B-Instruct-GGUF",
            description="Meta Llama 3.1 8B指令模型，多语言支持",
            parameters="8B",
            size_gb=5.0,
            quantization=QuantizationType.Q4_K_M,
            format=ModelFormat.GGUF,
            context_length=128000,
            tags=["llama", "meta", "instruct", "large", "multilingual"],
            benchmark_score=68.0,
        ),
        # Phi 4 系列
        ModelInfo(
            id="phi-4",
            name="Phi-4",
            repo_id="microsoft/phi-4-gguf",
            description="Microsoft Phi-4 14B级别性能，小巧高效",
            parameters="14B",
            size_gb=8.0,
            quantization=QuantizationType.Q4_K_M,
            format=ModelFormat.GGUF,
            context_length=16384,
            is_code_optimized=True,
            tags=["phi", "microsoft", "instruct", "code", "efficient"],
            benchmark_score=75.0,
        ),
        # DeepSeek 系列
        ModelInfo(
            id="deepseek-coder-6.7b",
            name="DeepSeek Coder 6.7B",
            repo_id="TheBloke/deepseek-coder-6.7b-instruct-GGUF",
            description="DeepSeek Coder 6.7B，代码能力优秀",
            parameters="6.7B",
            size_gb=4.0,
            quantization=QuantizationType.Q4_K_M,
            format=ModelFormat.GGUF,
            context_length=16384,
            is_code_optimized=True,
            is_chinese_optimized=True,
            tags=["deepseek", "coder", "code", "chinese"],
            benchmark_score=65.0,
        ),
        ModelInfo(
            id="deepseek-llm-7b",
            name="DeepSeek LLM 7B",
            repo_id="TheBloke/deepseek-llm-7b-chat-GGUF",
            description="DeepSeek 7B Chat模型，中文对话优化",
            parameters="7B",
            size_gb=4.5,
            quantization=QuantizationType.Q4_K_M,
            format=ModelFormat.GGUF,
            context_length=4096,
            is_chinese_optimized=True,
            tags=["deepseek", "chat", "chinese", "conversation"],
            benchmark_score=66.0,
        ),
        # Gemma 2 系列
        ModelInfo(
            id="gemma-2-2b",
            name="Gemma 2 2B",
            repo_id="bartowski/gemma-2-2b-it-GGUF",
            description="Google Gemma 2 2B指令模型，轻量高效",
            parameters="2B",
            size_gb=1.6,
            quantization=QuantizationType.Q4_K_M,
            format=ModelFormat.GGUF,
            context_length=8192,
            tags=["gemma", "google", "instruct", "small"],
            benchmark_score=58.0,
        ),
        ModelInfo(
            id="gemma-2-9b",
            name="Gemma 2 9B",
            repo_id="bartowski/gemma-2-9b-it-GGUF",
            description="Google Gemma 2 9B指令模型，知识丰富",
            parameters="9B",
            size_gb=6.0,
            quantization=QuantizationType.Q4_K_M,
            format=ModelFormat.GGUF,
            context_length=8192,
            tags=["gemma", "google", "instruct", "large"],
            benchmark_score=72.0,
        ),
        # Mistral 系列
        ModelInfo(
            id="mistral-7b",
            name="Mistral 7B",
            repo_id="TheBloke/Mistral-7B-Instruct-v0.3-GGUF",
            description="Mistral 7B Instruct v0.3，推理能力强",
            parameters="7B",
            size_gb=4.5,
            quantization=QuantizationType.Q4_K_M,
            format=ModelFormat.GGUF,
            context_length=32768,
            tags=["mistral", "instruct", "reasoning"],
            benchmark_score=67.0,
        ),
        # Yi 系列
        ModelInfo(
            id="yi-1.5-6b",
            name="Yi-1.5 6B",
            repo_id="TheBloke/Yi-1.5-6B-Chat-GGUF",
            description="零一万物 Yi-1.5 6B，中文对话",
            parameters="6B",
            size_gb=3.8,
            quantization=QuantizationType.Q4_K_M,
            format=ModelFormat.GGUF,
            context_length=4096,
            is_chinese_optimized=True,
            tags=["yi", "01-ai", "chinese", "chat"],
            benchmark_score=63.0,
        ),
        ModelInfo(
            id="yi-1.5-9b",
            name="Yi-1.5 9B",
            repo_id="TheBloke/Yi-1.5-9B-Chat-GGUF",
            description="零一万物 Yi-1.5 9B，中文长文本",
            parameters="9B",
            size_gb=5.8,
            quantization=QuantizationType.Q4_K_M,
            format=ModelFormat.GGUF,
            context_length=4096,
            is_chinese_optimized=True,
            tags=["yi", "01-ai", "chinese", "chat"],
            benchmark_score=69.0,
        ),
    ]

    def __init__(self) -> None:
        """初始化模型数据库"""
        self.models = self.MODELS.copy()

    def get_all_models(self) -> list[ModelInfo]:
        """获取所有模型"""
        return self.models

    def get_model_by_id(self, model_id: str) -> ModelInfo | None:
        """根据ID获取模型"""
        for model in self.models:
            if model.id == model_id:
                return model
        return None

    def filter_by_vram(self, max_vram_gb: float) -> list[ModelInfo]:
        """根据显存过滤模型"""
        return [m for m in self.models if m.size_gb <= max_vram_gb * 0.8]

    def filter_by_tags(self, tags: list[str]) -> list[ModelInfo]:
        """根据标签过滤模型"""
        if not tags:
            return self.models
        return [
            m for m in self.models
            if any(tag.lower() in t.lower() for tag in tags for t in m.tags)
        ]

    def get_chinese_optimized(self) -> list[ModelInfo]:
        """获取中文优化模型"""
        return [m for m in self.models if m.is_chinese_optimized]

    def get_code_optimized(self) -> list[ModelInfo]:
        """获取代码优化模型"""
        return [m for m in self.models if m.is_code_optimized]
