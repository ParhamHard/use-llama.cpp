# AI Room Project Dockerfile with GPU Support
# Based on Ubuntu base image for compatibility

FROM ubuntu:22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3.10-dev \
    python3-pip \
    python3.10-venv \
    git \
    wget \
    curl \
    build-essential \
    cmake \
    pkg-config \
    libopenblas-dev \
    liblapack-dev \
    libhdf5-dev \
    libssl-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Create symbolic link for python
RUN ln -s /usr/bin/python3.10 /usr/bin/python

# Upgrade pip
RUN python -m pip install --upgrade pip setuptools wheel

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Install PyTorch with CUDA support
RUN pip install "torch>=2.2.0,<3.0.0" --index-url https://download.pytorch.org/whl/cu121

# Install llama-cpp-python with GPU support
RUN CMAKE_ARGS="-DLLAMA_CUBLAS=on -DLLAMA_CUDA_F16=on" pip install llama-cpp-python>=0.3.16

# Copy project files
COPY . .

# Install the project in development mode
RUN pip install -e .

# Create a directory for models (you can mount this as a volume)
RUN mkdir -p /app/models

# Create a startup script
RUN echo '#!/bin/bash\n\
echo "🚀 Starting AI Room with GPU support..."\n\
echo "🔍 Checking GPU availability..."\n\
if command -v nvidia-smi &> /dev/null; then\n\
    nvidia-smi\n\
else\n\
    echo "⚠️  NVIDIA drivers not available, running in CPU mode"\n\
fi\n\
echo "🐍 Starting Python application..."\n\
echo "💡 Use: use-llama-cpp /path/to/model.gguf --interactive"\n\
echo "💡 Or run: python examples/basic_usage.py"\n\
bash\n\
' > /app/start.sh && chmod +x /app/start.sh

# Expose port if needed (for web interface)
EXPOSE 8000

# Set the default command
CMD ["/app/start.sh"]
