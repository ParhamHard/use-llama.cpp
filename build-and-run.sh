#!/bin/bash

# Use Llama.cpp Docker Build and Run Script
# This script builds and runs the Use Llama.cpp container with GPU support

set -e

echo "🚀 Use Llama.cpp Docker Build and Run Script"
echo "============================================"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check if nvidia-docker is available
if ! docker run --rm --gpus all nvidia/cuda:12.1-base-ubuntu22.04 nvidia-smi > /dev/null 2>&1; then
    echo "⚠️  NVIDIA Docker runtime not detected. GPU support may not work."
    echo "💡 Install nvidia-docker2 for full GPU support."
    read -p "Continue without GPU support? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
    GPU_SUPPORT=false
else
    echo "✅ NVIDIA Docker runtime detected. GPU support available."
    GPU_SUPPORT=true
fi

# Create models directory if it doesn't exist
if [ ! -d "models" ]; then
    echo "📁 Creating models directory..."
    mkdir -p models
    echo "💡 Place your .gguf model files in the models/ directory"
fi

# Build the container
echo "🔨 Building Docker container..."
docker-compose build

if [ $? -eq 0 ]; then
    echo "✅ Container built successfully!"
else
    echo "❌ Build failed. Check the error messages above."
    exit 1
fi

# Ask user what to do next
echo ""
echo "🎯 What would you like to do next?"
echo "1) Run with GPU support (recommended)"
echo "2) Run in background with GPU support"
echo "3) Run in development mode (no GPU)"
echo "4) Just build, don't run"
echo "5) Exit"

read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        echo "🚀 Starting Use Llama.cpp with GPU support..."
        docker-compose up use-llama-cpp
        ;;
    2)
        echo "🚀 Starting Use Llama.cpp in background with GPU support..."
        docker-compose up -d use-llama-cpp
        echo "✅ Container started in background."
        echo "📋 View logs: docker-compose logs -f use-llama-cpp"
        echo "🛑 Stop container: docker-compose down"
        ;;
    3)
        echo "🚀 Starting Use Llama.cpp in development mode..."
        docker-compose --profile dev up use-llama-cpp-dev
        ;;
    4)
        echo "✅ Container built successfully. Run it later with:"
        echo "   docker-compose up use-llama-cpp"
        ;;
    5)
        echo "👋 Exiting..."
        exit 0
        ;;
    *)
        echo "❌ Invalid choice. Exiting..."
        exit 1
        ;;
esac

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📚 Useful commands:"
echo "   View logs: docker-compose logs -f use-llama-cpp"
echo "   Stop container: docker-compose down"
echo "   Restart: docker-compose restart use-llama-cpp"
echo "   Shell access: docker exec -it use-llama-cpp-gpu bash"
echo ""
echo "🔧 For troubleshooting, see README-Docker.md"
