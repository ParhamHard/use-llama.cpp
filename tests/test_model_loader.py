"""
Tests for the ModelLoader class.
"""

import pytest
from unittest.mock import Mock, patch
from pathlib import Path

from use_llama_cpp.core.model_loader import ModelLoader


class TestModelLoader:
    """Test cases for ModelLoader class."""
    
    def test_init(self):
        """Test ModelLoader initialization."""
        loader = ModelLoader("/path/to/model.gguf", gpu_layers=10, context_size=1024)
        
        assert loader.model_path == "/path/to/model.gguf"
        assert loader.gpu_layers == 10
        assert loader.context_size == 1024
        assert loader.model is None
    
    def test_validate_model_path_not_exists(self):
        """Test model path validation when file doesn't exist."""
        loader = ModelLoader("/nonexistent/model.gguf")
        
        with patch('use_llama_cpp.core.model_loader.logger') as mock_logger:
            result = loader.validate_model_path()
            
            assert result is False
            mock_logger.error.assert_called_once()
    
    @patch('pathlib.Path.exists')
    @patch('pathlib.Path.is_file')
    @patch('os.path.getsize')
    def test_validate_model_path_success(self, mock_getsize, mock_is_file, mock_exists):
        """Test successful model path validation."""
        mock_exists.return_value = True
        mock_is_file.return_value = True
        mock_getsize.return_value = 1024 * 1024 * 1024  # 1GB
        
        loader = ModelLoader("/path/to/model.gguf")
        
        with patch('use_llama_cpp.core.model_loader.logger') as mock_logger:
            result = loader.validate_model_path()
            
            assert result is True
            mock_logger.info.assert_called()
    
    def test_is_loaded_false(self):
        """Test is_loaded when model is not loaded."""
        loader = ModelLoader("/path/to/model.gguf")
        assert loader.is_loaded() is False
    
    def test_is_loaded_true(self):
        """Test is_loaded when model is loaded."""
        loader = ModelLoader("/path/to/model.gguf")
        loader.model = Mock()
        assert loader.is_loaded() is True
    
    def test_unload_model(self):
        """Test model unloading."""
        loader = ModelLoader("/path/to/model.gguf")
        loader.model = Mock()
        
        with patch('use_llama_cpp.core.model_loader.logger') as mock_logger:
            loader.unload_model()
            
            assert loader.model is None
            mock_logger.info.assert_called_once_with("Model unloaded")


if __name__ == "__main__":
    pytest.main([__file__])
