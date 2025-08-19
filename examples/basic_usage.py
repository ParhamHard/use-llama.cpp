#!/usr/bin/env python3
"""
Basic usage example for AI Room.

This example demonstrates how to load a model and start chatting.
"""

import logging
from pathlib import Path

from airoom import ModelLoader, AIChat

# Setup logging
logging.basicConfig(level=logging.INFO)

def main():
    """Basic usage example."""
    # Model path - update this to your actual model file
    model_path = "/path/to/your/model.gguf"
    
    # Check if model exists
    if not Path(model_path).exists():
        print(f"❌ Model not found: {model_path}")
        print("💡 Please update the model_path variable with the correct path")
        return
    
    print("🚀 AI Room Basic Usage Example")
    print("=" * 40)
    
    # Initialize model loader
    print("📦 Initializing model loader...")
    loader = ModelLoader(
        model_path=model_path,
        gpu_layers=-1,  # Use all GPU layers
        context_size=2048
    )
    
    # Check GPU availability
    print("🔍 Checking GPU availability...")
    if loader.check_gpu_availability():
        print("✅ GPU acceleration available")
    else:
        print("⚠️  GPU acceleration not available, using CPU")
    
    # Load model
    print(f"\n🚀 Loading model: {Path(model_path).name}")
    model = loader.load_model()
    
    if not model:
        print("❌ Failed to load model")
        return
    
    print("✅ Model loaded successfully!")
    
    # Initialize chat
    print("\n💬 Initializing chat...")
    chat = AIChat(
        model,
        system_prompt="You are a helpful AI assistant. Keep your responses concise and relevant."
    )
    
    # Test conversation
    print("\n🧪 Testing conversation...")
    
    # First message
    response1 = chat.get_response("Hello! How are you today?")
    print(f"User: Hello! How are you today?")
    print(f"Assistant: {response1}")
    
    # Second message
    response2 = chat.get_response("What can you help me with?")
    print(f"\nUser: What can you help me with?")
    print(f"Assistant: {response2}")
    
    # Show conversation history
    print(f"\n📚 Conversation History:")
    history = chat.get_conversation_history()
    for i, msg in enumerate(history[1:], 1):  # Skip system prompt
        role = msg['role'].title()
        content = msg['content'][:80] + "..." if len(msg['content']) > 80 else msg['content']
        print(f"  {i}. {role}: {content}")
    
    # Cleanup
    print("\n🧹 Cleaning up...")
    loader.unload_model()
    print("✅ Example completed!")

if __name__ == "__main__":
    main()
