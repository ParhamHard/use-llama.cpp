# Use Llama.cpp Project Makefile
# Provides convenient commands for Docker operations

.PHONY: help build run run-bg stop logs shell clean dev test-gpu

# Default target
help:
	@echo "🚀 AI Room Project - Available Commands:"
	@echo ""
	@echo "📦 Build & Run:"
	@echo "  build        - Build the Docker container"
	@echo "  run          - Run container with GPU support (foreground)"
	@echo "  run-bg       - Run container with GPU support (background)"
	@echo "  dev          - Run in development mode (no GPU)"
	@echo ""
	@echo "🔧 Management:"
	@echo "  stop         - Stop and remove containers"
	@echo "  logs         - View container logs"
	@echo "  shell        - Access container shell"
	@echo "  restart      - Restart container"
	@echo ""
	@echo "🧹 Maintenance:"
	@echo "  clean        - Clean up Docker resources"
	@echo "  test-gpu     - Test GPU support"
	@echo ""
	@echo "📚 Documentation:"
	@echo "  help         - Show this help message"

# Build the container
build:
	@echo "🔨 Building AI Room container..."
	docker-compose build

# Run with GPU support (foreground)
run: build
	@echo "🚀 Starting AI Room with GPU support..."
	docker-compose up use-llama-cpp

# Run with GPU support (background)
run-bg: build
	@echo "🚀 Starting AI Room in background with GPU support..."
	docker-compose up -d use-llama-cpp
	@echo "✅ Container started in background"
	@echo "📋 View logs: make logs"
	@echo "🛑 Stop: make stop"

# Development mode (no GPU)
dev: build
	@echo "🚀 Starting AI Room in development mode..."
	docker-compose --profile dev up use-llama-cpp-dev

# Stop containers
stop:
	@echo "🛑 Stopping containers..."
	docker-compose down

# View logs
logs:
	@echo "📋 Viewing container logs..."
	docker-compose logs -f use-llama-cpp

# Access container shell
shell:
	@echo "🐚 Accessing container shell..."
	docker exec -it use-llama-cpp-gpu bash

# Restart container
restart:
	@echo "🔄 Restarting container..."
	docker-compose restart use-llama-cpp

# Clean up Docker resources
clean:
	@echo "🧹 Cleaning up Docker resources..."
	docker-compose down
	docker system prune -f
	docker volume prune -f

# Test GPU support
test-gpu:
	@echo "🧪 Testing GPU support..."
	docker run --rm --gpus all nvidia/cuda:12.1-base-ubuntu22.04 nvidia-smi

# Quick setup (build and run in background)
setup: build run-bg
	@echo "🎉 Setup complete! Container is running in background."
	@echo "📋 View logs: make logs"
	@echo "🛑 Stop: make stop"

# Show container status
status:
	@echo "📊 Container status:"
	docker-compose ps
	@echo ""
	@echo "📈 Resource usage:"
	docker stats --no-stream use-llama-cpp-gpu 2>/dev/null || echo "Container not running"
