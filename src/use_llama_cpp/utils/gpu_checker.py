"""
GPU availability and information checking utilities.
"""

import logging
import torch
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class GPUChecker:
    """Utility class for checking GPU availability and information."""
    
    @staticmethod
    def is_cuda_available() -> bool:
        """Check if CUDA is available."""
        return torch.cuda.is_available()
    
    @staticmethod
    def get_gpu_count() -> int:
        """Get the number of available GPUs."""
        if torch.cuda.is_available():
            return torch.cuda.device_count()
        return 0
    
    @staticmethod
    def get_gpu_info() -> List[Dict[str, any]]:
        """Get detailed information about all available GPUs."""
        gpu_info = []
        
        if not torch.cuda.is_available():
            return gpu_info
        
        for i in range(torch.cuda.device_count()):
            props = torch.cuda.get_device_properties(i)
            gpu_info.append({
                'index': i,
                'name': props.name,
                'memory_total_gb': props.total_memory / (1024**3),
                'memory_free_gb': torch.cuda.memory_reserved(i) / (1024**3),
                'compute_capability': f"{props.major}.{props.minor}",
                'multiprocessor_count': props.multi_processor_count
            })
        
        return gpu_info
    
    @staticmethod
    def get_current_gpu() -> Optional[int]:
        """Get the current GPU device index."""
        if torch.cuda.is_available():
            return torch.cuda.current_device()
        return None
    
    @staticmethod
    def set_gpu_device(device_index: int) -> bool:
        """Set the current GPU device."""
        if not torch.cuda.is_available():
            logger.warning("CUDA is not available")
            return False
        
        if device_index >= torch.cuda.device_count():
            logger.error(f"GPU device {device_index} does not exist")
            return False
        
        try:
            torch.cuda.set_device(device_index)
            logger.info(f"Set GPU device to {device_index}")
            return True
        except Exception as e:
            logger.error(f"Failed to set GPU device: {e}")
            return False
    
    @staticmethod
    def get_memory_info(device_index: int = None) -> Optional[Dict[str, float]]:
        """Get memory information for a specific GPU device."""
        if not torch.cuda.is_available():
            return None
        
        if device_index is None:
            device_index = torch.cuda.current_device()
        
        try:
            memory_allocated = torch.cuda.memory_allocated(device_index) / (1024**3)
            memory_reserved = torch.cuda.memory_reserved(device_index) / (1024**3)
            memory_free = torch.cuda.memory_reserved(device_index) / (1024**3)
            
            return {
                'allocated_gb': memory_allocated,
                'reserved_gb': memory_reserved,
                'free_gb': memory_free
            }
        except Exception as e:
            logger.error(f"Failed to get memory info: {e}")
            return None
    
    @staticmethod
    def print_gpu_summary():
        """Print a summary of GPU information."""
        if not torch.cuda.is_available():
            print("❌ CUDA is not available")
            return
        
        gpu_count = torch.cuda.device_count()
        print(f"✅ CUDA is available! Found {gpu_count} GPU(s)")
        
        for i in range(gpu_count):
            gpu_name = torch.cuda.get_device_name(i)
            gpu_memory = torch.cuda.get_device_properties(i).total_memory / (1024**3)
            print(f"   GPU {i}: {gpu_name} ({gpu_memory:.1f} GB)")
        
        current_device = torch.cuda.current_device()
        print(f"🎯 Using GPU device: {current_device}")
        
        # Print memory info for current device
        memory_info = GPUChecker.get_memory_info(current_device)
        if memory_info:
            print(f"💾 Memory - Allocated: {memory_info['allocated_gb']:.2f} GB, "
                  f"Reserved: {memory_info['reserved_gb']:.2f} GB")
