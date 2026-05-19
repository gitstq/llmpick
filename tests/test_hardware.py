"""硬件检测测试"""

import pytest

from llmpick.hardware import HardwareDetector
from llmpick.types import GPUVendor


class TestHardwareDetector:
    """测试硬件检测器"""

    def test_detector_initialization(self):
        """测试检测器初始化"""
        detector = HardwareDetector()
        assert detector is not None

    def test_detect_returns_hardware_info(self):
        """测试检测返回硬件信息"""
        detector = HardwareDetector()
        hardware = detector.detect()
        
        assert hardware.cpu_name
        assert hardware.cpu_cores > 0
        assert hardware.ram_gb > 0
        assert hardware.disk_free_gb > 0

    def test_format_hardware_info(self):
        """测试格式化硬件信息"""
        detector = HardwareDetector()
        hardware = detector.detect()
        formatted = detector.format_hardware_info(hardware)
        
        assert "CPU:" in formatted
        assert "内存:" in formatted
        assert "GPU信息:" in formatted


class TestGPUInfo:
    """测试GPU信息"""

    def test_total_vram_calculation(self):
        """测试总显存计算"""
        from llmpick.types import GPUInfo, HardwareInfo
        
        gpus = [
            GPUInfo(name="GPU1", vendor=GPUVendor.NVIDIA, vram_gb=8.0),
            GPUInfo(name="GPU2", vendor=GPUVendor.NVIDIA, vram_gb=8.0),
        ]
        hardware = HardwareInfo(
            cpu_name="Test CPU",
            cpu_cores=8,
            ram_gb=16.0,
            disk_free_gb=100.0,
            gpus=gpus,
        )
        
        assert hardware.total_vram_gb == 16.0

    def test_primary_gpu_selection(self):
        """测试主GPU选择"""
        from llmpick.types import GPUInfo, HardwareInfo
        
        gpus = [
            GPUInfo(name="Integrated", vendor=GPUVendor.INTEL, vram_gb=2.0, is_integrated=True),
            GPUInfo(name="Dedicated", vendor=GPUVendor.NVIDIA, vram_gb=8.0),
        ]
        hardware = HardwareInfo(
            cpu_name="Test CPU",
            cpu_cores=8,
            ram_gb=16.0,
            disk_free_gb=100.0,
            gpus=gpus,
        )
        
        assert hardware.primary_gpu is not None
        assert hardware.primary_gpu.name == "Dedicated"
