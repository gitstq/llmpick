"""LLMPick - 智能本地LLM选型助手

Intelligent Local LLM Selector and Recommendation Engine
"""

__version__ = "1.0.0"
__author__ = "LLMPick Team"
__email__ = "llmpick@example.com"

from llmpick.core import LLMPick
from llmpick.hardware import HardwareDetector
from llmpick.models import ModelDatabase

__all__ = ["LLMPick", "HardwareDetector", "ModelDatabase"]
