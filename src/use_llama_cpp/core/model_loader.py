"""
Model loader for AI Room application with GPU acceleration support.
"""

import os
import logging
from typing import Optional, Dict, Any
from llama_cpp import Llama
import torch

logger = logging.getLogger(__name__)


class ModelLoader:
    """Handles loading and management of GGUF models with GPU acceleration."""
    
    def __init__(self, model_path: str, gpu_layers: int = -1, context_size: int = 2048):
        """
        Initialize the model loader.
        
        Args:
            model_path: Path to the GGUF model file
            gpu_layers: Number of GPU layers to use (-1 for all, 0 for CPU only)
            context_size: Context window size
        """
        self.model_path = model_path
        self.gpu_layers = gpu_layers
        self.context_size = context_size
        self.model: Optional[Llama] = None
        
    def validate_model_path(self) -> bool:
        """Validate that the model file exists and is accessible."""
        if not os.path.exists(self.model_path):
            logger.error(f"Model file not found: {self.model_path}")
            return False
        
        if not self.model_path.endswith('.gguf'):
            logger.warning(f"Model file doesn't have .gguf extension: {self.model_path}")
        
        file_size = os.path.getsize(self.model_path) / (1024 * 1024 * 1024)  # Size in GB
        logger.info(f"Model file found: {os.path.basename(self.model_path)}")
        logger.info(f"File size: {file_size:.2f} GB")
        
        return True
    
    def check_gpu_availability(self) -> bool:
        """Check if GPU is available and provide information."""
        logger.info("Checking GPU availability...")
        
        if torch.cuda.is_available():
            gpu_count = torch.cuda.device_count()
            logger.info(f"CUDA is available! Found {gpu_count} GPU(s)")
            
            for i in range(gpu_count):
                gpu_name = torch.cuda.get_device_name(i)
                gpu_memory = torch.cuda.get_device_properties(i).total_memory / (1024**3)
                logger.info(f"GPU {i}: {gpu_name} ({gpu_memory:.1f} GB)")
            
            torch.cuda.set_device(0)
            logger.info(f"Using GPU device: {torch.cuda.current_device()}")
            return True
        else:
            logger.warning("CUDA is not available")
            return False
    
    def load_model(self) -> Optional[Llama]:
        """Load a GGUF model with GPU acceleration."""
        if not self.validate_model_path():
            return None
        
        logger.info(f"Loading model: {os.path.basename(self.model_path)}")
        logger.info(f"GPU layers: {self.gpu_layers}")
        logger.info(f"Context size: {self.context_size}")
        
        try:
            self.model = Llama(
                model_path=self.model_path,
                n_gpu_layers=self.gpu_layers,
                n_ctx=self.context_size,
                n_batch=512,
                verbose=False,
                offload_kqv=True,
                mul_mat_q=True,
            )
            
            logger.info("Model loaded successfully!")
            
            if self.gpu_layers > 0:
                logger.info(f"Model configured to use {self.gpu_layers} GPU layers")
            elif self.gpu_layers == -1:
                logger.info("Model configured to use ALL layers on GPU")
            else:
                logger.warning("Model configured for CPU-only usage")
                
            return self.model
            
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            return None
    
    def get_model(self) -> Optional[Llama]:
        """Get the loaded model instance."""
        if self.model is None:
            self.model = self.load_model()
        return self.model
    
    def is_loaded(self) -> bool:
        """Check if the model is loaded."""
        return self.model is not None
    
    def unload_model(self):
        """Unload the model to free memory."""
        if self.model:
            del self.model
            self.model = None
            logger.info("Model unloaded")
