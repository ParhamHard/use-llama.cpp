"""
AI Room - A GPU-accelerated AI chat application using llama.cpp

A powerful, lightweight AI chat application that leverages GPU acceleration
for fast and efficient language model inference.
"""

__version__ = "0.1.0"
__author__ = "Parham Hard"
__description__ = "GPU-accelerated AI chat application using llama.cpp"

from .core.chat import AIChat
from .core.model_loader import ModelLoader
from .utils.gpu_checker import GPUChecker

__all__ = [
    "AIChat",
    "ModelLoader", 
    "GPUChecker",
    "__version__",
    "__author__",
    "__description__"
]
