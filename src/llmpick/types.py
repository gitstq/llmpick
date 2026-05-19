"""类型定义模块"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class GPUVendor(Enum):
    """GPU厂商"""
    NVIDIA = "nvidia"
    AMD = "amd"
    INTEL = "intel"
    APPLE = "apple"
    UNKNOWN = "unknown"


class QuantizationType(Enum):
    """量化类型"""
    Q4_0 = "Q4_0"
    Q4_K_M = "Q4_K_M"
    Q5_0 = "Q5_0"
    Q5_K_M = "Q5_K_M"
    Q6_K = "Q6_K"
    Q8_0 = "Q8_0"
    FP16 = "FP16"
    FP32 = "FP32"


class ModelFormat(Enum):
    """模型格式"""
    GGUF = "gguf"
    AWQ = "awq"
    GPTQ = "gptq"
    SAFETENSORS = "safetensors"
    PYTORCH = "pytorch"


@dataclass
class GPUInfo:
    """GPU信息"""
    name: str
    vendor: GPUVendor
    vram_gb: float
    compute_capability: Optional[str] = None
    is_integrated: bool = False


@dataclass
class HardwareInfo:
    """硬件信息"""
    cpu_name: str
    cpu_cores: int
    ram_gb: float
    disk_free_gb: float
    gpus: list[GPUInfo] = field(default_factory=list)
    os_name: str = ""
    os_version: str = ""
    has_cuda: bool = False
    has_metal: bool = False
    has_rocm: bool = False

    @property
    def total_vram_gb(self) -> float:
        """总显存（GB）"""
        return sum(gpu.vram_gb for gpu in self.gpus)

    @property
    def primary_gpu(self) -> Optional[GPUInfo]:
        """主GPU"""
        if self.gpus:
            # 优先选择独立显卡
            dedicated = [g for g in self.gpus if not g.is_integrated]
            return dedicated[0] if dedicated else self.gpus[0]
        return None


@dataclass
class ModelInfo:
    """模型信息"""
    id: str
    name: str
    repo_id: str
    description: str
    parameters: str  # e.g., "7B", "13B"
    size_gb: float
    quantization: QuantizationType
    format: ModelFormat
    context_length: int
    is_multimodal: bool = False
    is_code_optimized: bool = False
    is_chinese_optimized: bool = False
    download_url: str = ""
    tags: list[str] = field(default_factory=list)
    benchmark_score: Optional[float] = None


@dataclass
class Recommendation:
    """推荐结果"""
    model: ModelInfo
    score: float  # 0-100
    fit_type: str  # "perfect", "good", "partial", "cpu_only"
    estimated_tokens_per_sec: float
    vram_usage_gb: float
    reason: str
