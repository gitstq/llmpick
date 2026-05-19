"""硬件检测模块"""

from __future__ import annotations

import platform
import subprocess
from typing import Optional

import psutil

from llmpick.types import GPUInfo, GPUVendor, HardwareInfo


class HardwareDetector:
    """硬件检测器"""

    def detect(self) -> HardwareInfo:
        """检测硬件信息"""
        return HardwareInfo(
            cpu_name=self._detect_cpu(),
            cpu_cores=psutil.cpu_count(logical=True) or 1,
            ram_gb=psutil.virtual_memory().total / (1024**3),
            disk_free_gb=psutil.disk_usage("/").free / (1024**3),
            gpus=self._detect_gpus(),
            os_name=platform.system(),
            os_version=platform.release(),
            has_cuda=self._check_cuda(),
            has_metal=self._check_metal(),
            has_rocm=self._check_rocm(),
        )

    def _detect_cpu(self) -> str:
        """检测CPU型号"""
        try:
            if platform.system() == "Darwin":
                result = subprocess.run(
                    ["sysctl", "-n", "machdep.cpu.brand_string"],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                return result.stdout.strip()
            elif platform.system() == "Linux":
                with open("/proc/cpuinfo", "r") as f:
                    for line in f:
                        if "model name" in line:
                            return line.split(":")[1].strip()
            return platform.processor() or "Unknown CPU"
        except Exception:
            return "Unknown CPU"

    def _detect_gpus(self) -> list[GPUInfo]:
        """检测GPU信息"""
        gpus = []
        
        # 尝试检测NVIDIA GPU
        nvidia_gpus = self._detect_nvidia_gpus()
        gpus.extend(nvidia_gpus)
        
        # 尝试检测Apple Silicon
        if platform.system() == "Darwin":
            apple_gpu = self._detect_apple_gpu()
            if apple_gpu:
                gpus.append(apple_gpu)
        
        return gpus

    def _detect_nvidia_gpus(self) -> list[GPUInfo]:
        """检测NVIDIA GPU"""
        gpus = []
        try:
            result = subprocess.run(
                ["nvidia-smi", "--query-gpu=name,memory.total,compute_cap", "--format=csv,noheader"],
                capture_output=True,
                text=True,
                check=True,
            )
            for line in result.stdout.strip().split("\n"):
                if line:
                    parts = [p.strip() for p in line.split(",")]
                    if len(parts) >= 2:
                        name = parts[0]
                        # 解析显存大小
                        mem_str = parts[1]
                        if "MiB" in mem_str:
                            vram_gb = int(mem_str.replace("MiB", "").strip()) / 1024
                        elif "GiB" in mem_str:
                            vram_gb = float(mem_str.replace("GiB", "").strip())
                        else:
                            vram_gb = 0.0
                        
                        compute_cap = parts[2] if len(parts) > 2 else None
                        
                        gpus.append(GPUInfo(
                            name=name,
                            vendor=GPUVendor.NVIDIA,
                            vram_gb=vram_gb,
                            compute_capability=compute_cap,
                        ))
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
        return gpus

    def _detect_apple_gpu(self) -> Optional[GPUInfo]:
        """检测Apple Silicon GPU"""
        try:
            # 检测是否为Apple Silicon
            result = subprocess.run(
                ["sysctl", "-n", "hw.optional.arm64"],
                capture_output=True,
                text=True,
                check=True,
            )
            if result.stdout.strip() == "1":
                # 获取内存作为统一内存
                mem_result = subprocess.run(
                    ["sysctl", "-n", "hw.memsize"],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                total_mem_bytes = int(mem_result.stdout.strip())
                total_mem_gb = total_mem_bytes / (1024**3)
                
                # 获取芯片型号
                chip_result = subprocess.run(
                    ["sysctl", "-n", "machdep.cpu.brand_string"],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                chip_name = chip_result.stdout.strip()
                
                return GPUInfo(
                    name=f"Apple {chip_name} GPU",
                    vendor=GPUVendor.APPLE,
                    vram_gb=total_mem_gb * 0.6,  # 约60%可作为GPU内存
                    is_integrated=True,
                )
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
        return None

    def _check_cuda(self) -> bool:
        """检查是否支持CUDA"""
        try:
            subprocess.run(
                ["nvidia-smi"],
                capture_output=True,
                check=True,
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def _check_metal(self) -> bool:
        """检查是否支持Metal"""
        return platform.system() == "Darwin" and platform.machine() == "arm64"

    def _check_rocm(self) -> bool:
        """检查是否支持ROCm"""
        try:
            subprocess.run(
                ["rocminfo"],
                capture_output=True,
                check=True,
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def format_hardware_info(self, hardware: HardwareInfo) -> str:
        """格式化硬件信息为字符串"""
        lines = [
            f"CPU: {hardware.cpu_name}",
            f"CPU核心数: {hardware.cpu_cores}",
            f"内存: {hardware.ram_gb:.1f} GB",
            f"磁盘可用: {hardware.disk_free_gb:.1f} GB",
            f"操作系统: {hardware.os_name} {hardware.os_version}",
            "",
            "GPU信息:",
        ]
        
        if hardware.gpus:
            for i, gpu in enumerate(hardware.gpus, 1):
                lines.append(f"  [{i}] {gpu.name}")
                lines.append(f"      显存: {gpu.vram_gb:.1f} GB")
                if gpu.compute_capability:
                    lines.append(f"      计算能力: {gpu.compute_capability}")
        else:
            lines.append("  未检测到独立GPU，将使用CPU运行")
        
        lines.append("")
        lines.append("加速支持:")
        lines.append(f"  CUDA: {'✓' if hardware.has_cuda else '✗'}")
        lines.append(f"  Metal: {'✓' if hardware.has_metal else '✗'}")
        lines.append(f"  ROCm: {'✓' if hardware.has_rocm else '✗'}")
        
        return "\n".join(lines)
