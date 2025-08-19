#!/bin/bash
# Environment setup script for AI Room project
# This script ensures all dependencies are properly installed with compatible versions

echo "🚀 Setting up AI Room environment..."

# Check if conda is available
if ! command -v conda &> /dev/null; then
    echo "❌ Conda is not installed or not in PATH"
    echo "💡 Please install Miniconda or Anaconda first"
    exit 1
fi

# Check if aivenv environment exists
if conda env list | grep -q "aivenv"; then
    echo "✅ Found existing aivenv environment"
else
    echo "🔧 Creating new aivenv environment..."
    conda create -n aivenv python=3.10 -y
fi

# Activate environment
echo "🔧 Activating aivenv environment..."
source $(conda info --base)/etc/profile.d/conda.sh
conda activate aivenv

# Remove conflicting packages if they exist
echo "🧹 Cleaning up conflicting packages..."
pip uninstall numpy torch -y 2>/dev/null || true

# Install compatible versions
echo "📦 Installing compatible numpy version..."
pip install "numpy>=1.25.0,<2.0.0"

echo "📦 Installing compatible torch version..."
pip install "torch>=2.2.0,<3.0.0" --index-url https://download.pytorch.org/whl/cu121

echo "📦 Installing other requirements..."
pip install -r requirements.txt

# Verify installation
echo "🔍 Verifying installation..."
python test_dependencies.py

echo ""
echo "🎉 Environment setup complete!"
echo "💡 To activate the environment in the future, run: conda activate aivenv"
echo "💡 To run your AI chat: python main.py"
