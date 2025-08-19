# AI Room Docker Setup

This Docker setup provides a containerized environment for running the AI Room project with GPU acceleration support.

## Prerequisites

### 1. Docker and Docker Compose
Make sure you have Docker and Docker Compose installed:
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 2. NVIDIA Docker Runtime
For GPU support, install NVIDIA Docker runtime:
```bash
# Add NVIDIA package repositories
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

# Install nvidia-docker2
sudo apt-get update
sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker
```

### 3. NVIDIA Drivers
Ensure you have NVIDIA drivers installed:
```bash
nvidia-smi
```

## Quick Start

### 1. Build and Run with GPU Support
```bash
# Build the container
docker-compose build

# Run with GPU support
docker-compose up airoom
```

### 2. Run in Background
```bash
docker-compose up -d airoom
```

### 3. View Logs
```bash
docker-compose logs -f airoom
```

### 4. Stop the Container
```bash
docker-compose down
```

## Configuration

### Model Path
Update the model path in your Python files to point to the mounted volume:
```python
# In main.py or load_model_gpu.py, change:
MODEL_PATH = "/app/models/your_model.gguf"
```

### Mounting Models
You can mount your model files in several ways:

1. **Mount entire models directory:**
   ```bash
   # Create a models directory
   mkdir -p models
   
   # Copy your .gguf files there
   cp /path/to/your/model.gguf models/
   ```

2. **Mount specific model file:**
   ```yaml
   # In docker-compose.yml, uncomment and modify:
   volumes:
     - /path/to/your/model.gguf:/app/models/model.gguf
   ```

3. **Use environment variable:**
   ```bash
   docker run -e MODEL_PATH=/app/models/model.gguf ...
   ```

## Development Mode

For development without GPU:
```bash
docker-compose --profile dev up airoom-dev
```

## Troubleshooting

### GPU Not Detected
1. Check if NVIDIA Docker runtime is installed:
   ```bash
   docker run --rm --gpus all nvidia/cuda:12.1-base-ubuntu22.04 nvidia-smi
   ```

2. Verify Docker has access to GPU:
   ```bash
   docker run --rm --gpus all nvidia/cuda:12.1-base-ubuntu22.04 nvidia-smi
   ```

### Build Issues
1. Clear Docker cache:
   ```bash
   docker system prune -a
   ```

2. Rebuild without cache:
   ```bash
   docker-compose build --no-cache
   ```

### Memory Issues
If you encounter GPU memory issues:
1. Reduce batch size in your Python code
2. Use fewer GPU layers: `n_gpu_layers=10` instead of `-1`
3. Monitor GPU memory: `nvidia-smi`

## Performance Tips

1. **Use GPU layers efficiently:**
   ```python
   # Use specific number of layers instead of all
   n_gpu_layers=20  # Adjust based on your GPU memory
   ```

2. **Optimize context size:**
   ```python
   n_ctx=1024  # Smaller context for less memory usage
   ```

3. **Batch processing:**
   ```python
   n_batch=256  # Smaller batch size for less memory
   ```

## Environment Variables

You can customize the container behavior with environment variables:

```bash
# In docker-compose.yml or docker run command:
environment:
  - MODEL_PATH=/app/models/model.gguf
  - GPU_LAYERS=20
  - CONTEXT_SIZE=1024
  - MAX_TOKENS=256
```

## Monitoring

### GPU Usage
```bash
# Inside container
nvidia-smi

# From host
docker exec airoom-gpu nvidia-smi
```

### Container Stats
```bash
docker stats airoom-gpu
```

### Logs
```bash
docker-compose logs -f airoom
```

## Security Notes

- The container runs as root by default
- Consider creating a non-root user for production
- Be careful with volume mounts to avoid exposing sensitive data
- Use `.dockerignore` to exclude unnecessary files

## Support

If you encounter issues:
1. Check the logs: `docker-compose logs airoom`
2. Verify GPU support: `nvidia-smi`
3. Test basic CUDA: `docker run --rm --gpus all nvidia/cuda:12.1-base-ubuntu22.04 nvidia-smi`
4. Check Docker version: `docker --version`
5. Verify NVIDIA Docker runtime: `docker info | grep nvidia`
