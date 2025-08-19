# AI Room 🚀

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/use-llama.cpp.svg)](https://badge.fury.io/py/use-llama.cpp)
[![Documentation](https://readthedocs.org/projects/use-llama-cpp/badge/?version=latest)](https://use-llama-cpp.readthedocs.io/)

A powerful, GPU-accelerated AI chat application that leverages llama.cpp for fast and efficient language model inference. Built with modern Python practices and designed for both developers and end-users.

## ✨ Features

- 🚀 **GPU Acceleration**: Full CUDA support with automatic GPU detection
- 🧠 **Multiple Models**: Support for any GGUF format language model
- 💬 **Interactive Chat**: Command-line interface with conversation history
- 🔧 **Configurable**: Customizable parameters for model behavior
- 📦 **Easy Installation**: Simple pip install or Docker deployment
- 🐳 **Container Ready**: Full Docker support with GPU passthrough
- 📚 **Well Documented**: Comprehensive documentation and examples

## 🚀 Quick Start

### Installation

```bash
# Install from PyPI
pip install use-llama.cpp

# Install with GPU support
pip install use-llama.cpp[gpu]

# Install development dependencies
pip install use-llama.cpp[dev]
```

### Basic Usage

```bash
# Run with a GGUF model
use-llama-cpp /path/to/your/model.gguf

# Interactive chat mode
use-llama-cpp /path/to/your/model.gguf --interactive

# Customize GPU layers and context
use-llama-cpp model.gguf --gpu-layers 20 --context-size 4096 --verbose
```

### Python API

```python
from use_llama_cpp import ModelLoader, AIChat

# Load model with GPU acceleration
loader = ModelLoader("/path/to/model.gguf", gpu_layers=-1)
model = loader.load_model()

# Start chatting
chat = AIChat(model)
response = chat.get_response("Hello! How are you today?")
print(response)
```

## 🐳 Docker Usage

### Quick Start with Docker

```bash
# Build and run with GPU support
docker-compose up use-llama-cpp

# Or use the convenience script
./build-and-run.sh
```

### Docker Commands

```bash
# Build the container
make build

# Run with GPU support
make run

# Run in background
make run-bg

# View logs
make logs

# Stop container
make stop
```

## 📖 Documentation

- [📚 Full Documentation](https://use-llama-cpp.readthedocs.io/)
- [🐳 Docker Guide](README-Docker.md)
- [🔧 API Reference](docs/api.md)
- [📝 Examples](examples/)
- [🧪 Testing](tests/)

## 🛠️ Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/parhamhard/use-llama.cpp.git
cd use-llama.cpp

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=use_llama_cpp

# Run specific test file
pytest tests/test_model_loader.py
```

### Code Quality

```bash
# Format code
black src/ tests/

# Lint code
pylint src/use_llama_cpp/

# Type checking
mypy src/use_llama_cpp/
```

## 📁 Project Structure

```
use-llama.cpp/
├── src/use_llama_cpp/   # Source code
│   ├── core/            # Core functionality
│   │   ├── chat.py      # Chat interface
│   │   └── model_loader.py  # Model loading
│   ├── cli/             # Command-line interface
│   ├── utils/           # Utility functions
│   └── __init__.py      # Package initialization
├── tests/               # Test suite
├── docs/                # Documentation
├── examples/            # Usage examples
├── scripts/             # Utility scripts
├── Dockerfile           # Docker configuration
├── docker-compose.yml   # Docker Compose
├── pyproject.toml       # Project configuration
└── README.md            # This file
```

## 🔧 Configuration

### Environment Variables

- `USE_LLAMA_CPP_MODEL_PATH`: Default model path
- `USE_LLAMA_CPP_GPU_LAYERS`: Default GPU layers (-1 for all)
- `USE_LLAMA_CPP_CONTEXT_SIZE`: Default context window size
- `USE_LLAMA_CPP_LOG_LEVEL`: Logging level (INFO, DEBUG, etc.)

### Model Parameters

- `--gpu-layers`: Number of GPU layers to use
- `--context-size`: Context window size
- `--max-tokens`: Maximum response length
- `--temperature`: Response randomness
- `--system-prompt`: Custom system prompt

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Workflow

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run the test suite
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [llama.cpp](https://github.com/ggerganov/llama.cpp) - Fast inference engine
- [llama-cpp-python](https://github.com/abetlen/llama-cpp-python) - Python bindings
- [PyTorch](https://pytorch.org/) - GPU acceleration support


---

**Made with ❤️ by the Use Llama.cpp Team**
