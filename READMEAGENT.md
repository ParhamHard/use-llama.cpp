# AI Agent Reference Guide

## Git and GitHub Operations

### Removing Old Commits from GitHub

There are several methods to remove old commits from GitHub, depending on your specific needs:

#### Method 1: Interactive Rebase (Recommended for few commits)
- **Best for**: Few commits, clean history
- **Command**: `git rebase -i --root` (for all commits) or `git rebase -i HEAD~n` (for last n commits)
- **Use case**: When you want to pick, edit, squash, or drop specific commits
- **Example**: `git rebase -i --root` then edit the file to drop unwanted commits

#### Method 2: Reset and Force Push
```bash
# Reset to a specific commit
git reset --hard <commit-hash>

# Force push to overwrite GitHub history (use --force-with-lease for safety)
git push --force-with-lease origin master
```

#### Method 3: Filter Branch (For complex history rewriting)
```bash
git filter-branch --index-filter 'git rm --cached --ignore-unmatch <file>' --prune-empty --tag-name-filter cat -- --all
```

#### Method 4: BFG Repo Cleaner (For large repositories)
```bash
# Install BFG first
java -jar bfg.jar --delete-files <filename> <repo>
```

### Important Notes:
- **Force pushing rewrites history** - use with caution
- **--force-with-lease** is safer than --force as it prevents overwriting others' work
- **Interactive rebase** is the cleanest method for small repositories
- **Always backup** your repository before major history changes
- **Communicate with team members** if working on shared repositories

### Current Repository Status:
- Repository: use-llama.cpp
- Remotes: GitHub and Gitea
- Current branch: master
- Recent commits: 3 commits (including initial commit and project rename)

### Common Use Cases:
1. **Remove sensitive information** from commit history
2. **Clean up messy commit history** before sharing
3. **Remove large files** that were accidentally committed
4. **Squash multiple commits** into one clean commit
5. **Remove commits** that contain bugs or incorrect information

### Safety Commands:
```bash
# Check current status
git status

# View commit history
git log --oneline

# Check remote status
git remote -v

# Backup current state
git branch backup-before-cleanup
```

## Testing use-llama.cpp Project

### Project Overview
**use-llama.cpp** is a GPU-accelerated AI chat application that leverages llama.cpp for fast and efficient language model inference. It's built with modern Python practices and designed for both developers and end-users.

### Key Features
- 🚀 GPU Acceleration with CUDA support
- 🧠 Support for GGUF format language models
- 💬 Interactive command-line chat interface
- 🔧 Configurable model parameters
- 📦 Easy installation via pip or Docker
- 🐳 Full Docker support with GPU passthrough

### Testing Approaches

#### 1. Quick Docker Test (Recommended for first-time users)
```bash
# Clone the repository
git clone <repository-url>
cd use-llama.cpp

# Make the build script executable
chmod +x build-and-run.sh

# Run the interactive build and run script
./build-and-run.sh
```

**What this does:**
- Checks Docker availability
- Detects NVIDIA GPU support
- Builds the Docker container
- Offers multiple run options (GPU, background, dev mode)
- Creates models directory for GGUF files

#### 2. Manual Docker Testing
```bash
# Build the container
docker-compose build

# Run with GPU support
docker-compose up use-llama-cpp

# Run in background
docker-compose up -d use-llama-cpp

# View logs
docker-compose logs -f use-llama-cpp

# Stop container
docker-compose down
```

#### 3. Local Python Testing
```bash
# Install in development mode
pip install -e .

# Install with GPU support
pip install -e .[gpu]

# Install development dependencies
pip install -e .[dev]

# Run tests
pytest tests/

# Run specific test
pytest tests/test_model_loader.py -v
```

#### 4. Manual Model Testing
```bash
# You need a GGUF model file first
# Download a small model for testing (e.g., from Hugging Face)

# Run the CLI tool
use-llama-cpp /path/to/your/model.gguf --interactive

# Or use Python API
python examples/basic_usage.py
```

### Required Dependencies

#### System Requirements
- **Python**: 3.10+
- **Docker**: For containerized testing
- **NVIDIA GPU**: For GPU acceleration (optional but recommended)
- **nvidia-docker2**: For GPU support in Docker

#### Python Dependencies
- `llama-cpp-python>=0.3.16`
- `torch>=2.2.0,<3.0.0`
- `numpy>=1.25.0,<2.0.0`
- `openai>=1.0.0`

### Testing Checklist

#### Pre-Test Setup
- [ ] Docker is running
- [ ] NVIDIA drivers installed (if using GPU)
- [ ] nvidia-docker2 installed (if using GPU)
- [ ] Python 3.10+ available
- [ ] GGUF model file available (for full testing)

#### Basic Functionality Tests
- [ ] Docker container builds successfully
- [ ] Container starts without errors
- [ ] GPU detection works (if applicable)
- [ ] Model loading works (with test model)
- [ ] Chat interface responds
- [ ] Python API imports correctly

#### Advanced Tests
- [ ] GPU acceleration works
- [ ] Different model parameters work
- [ ] Error handling for invalid models
- [ ] Memory management
- [ ] Performance benchmarks

### Common Issues and Solutions

#### Docker Issues
```bash
# If Docker isn't running
sudo systemctl start docker

# If nvidia-docker not available
sudo apt-get install nvidia-docker2
sudo systemctl restart docker

# If permission denied
sudo usermod -aG docker $USER
# Then logout and login again
```

#### GPU Issues
```bash
# Check NVIDIA drivers
nvidia-smi

# Check CUDA installation
nvcc --version

# Test nvidia-docker
docker run --rm --gpus all nvidia/cuda:12.1-base-ubuntu22.04 nvidia-smi
```

#### Python Issues
```bash
# If llama-cpp-python fails to install
pip install --upgrade pip setuptools wheel

# For GPU support, you might need to set environment variables
export CMAKE_ARGS="-DLLAMA_CUBLAS=on"
export FORCE_CMAKE=1
pip install llama-cpp-python
```

### Example Test Session

```bash
# 1. Clone and setup
git clone <repo-url>
cd use-llama.cpp

# 2. Quick Docker test
./build-and-run.sh
# Choose option 1 (Run with GPU support)

# 3. Test Python installation
pip install -e .[dev]
pytest tests/ -v

# 4. Test with actual model
# Download a small GGUF model (e.g., 7B parameter model)
# Place in models/ directory
# Run: use-llama-cpp models/your-model.gguf --interactive
```

### Expected Behavior
- **Docker**: Container should build and start without errors
- **GPU Detection**: Should detect NVIDIA GPU if available
- **Model Loading**: Should load GGUF models successfully
- **Chat Interface**: Should provide interactive chat experience
- **Performance**: Should be noticeably faster with GPU acceleration

### Troubleshooting Commands
```bash
# Check system resources
nvidia-smi
docker stats
htop

# Check container logs
docker-compose logs -f use-llama-cpp

# Check Python environment
python -c "import use_llama_cpp; print(use_llama_cpp.__version__)"

# Check model file
file /path/to/model.gguf
ls -lh /path/to/model.gguf
```

This testing guide should help future AI agents understand how to comprehensively test the use-llama.cpp project and troubleshoot common issues.
