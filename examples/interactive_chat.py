#!/usr/bin/env python3
"""
Interactive chat example for AI Room.

This example provides an interactive chat interface.
"""

import logging
import sys
from pathlib import Path

from airoom import ModelLoader, AIChat

# Setup logging
logging.basicConfig(level=logging.INFO)

def interactive_chat(chat: AIChat):
    """Run interactive chat mode."""
    print("\n💬 Interactive Chat Mode")
    print("=" * 30)
    print("💡 Type 'quit', 'exit', or 'q' to exit")
    print("💡 Type 'reset' to clear conversation history")
    print("💡 Type 'history' to view conversation history")
    print("💡 Type 'help' for available commands")
    print("💡 Type 'system' to change system prompt")
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
                
            if user_input.lower() == 'reset':
                chat.reset_conversation()
                print("🔄 Conversation history reset")
                continue
                
            if user_input.lower() == 'history':
                history = chat.get_conversation_history()
                print("\n📚 Conversation History:")
                for i, msg in enumerate(history[1:], 1):  # Skip system prompt
                    role = msg['role'].title()
                    content = msg['content'][:100] + "..." if len(msg['content']) > 100 else msg['content']
                    print(f"  {i}. {role}: {content}")
                continue
                
            if user_input.lower() == 'help':
                print("\n📖 Available Commands:")
                print("  quit/exit/q - Exit the chat")
                print("  reset - Clear conversation history")
                print("  history - View conversation history")
                print("  system - Change system prompt")
                print("  help - Show this help message")
                continue
                
            if user_input.lower() == 'system':
                new_prompt = input("Enter new system prompt: ").strip()
                if new_prompt:
                    chat.set_system_prompt(new_prompt)
                    print("✅ System prompt updated")
                continue
            
            # Get AI response
            print("🤔 Thinking...")
            response = chat.get_response(user_input)
            
            if response:
                print(f"Assistant: {response}")
            else:
                print("Assistant: I'm not sure how to respond to that.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def main():
    """Interactive chat example."""
    # Model path - update this to your actual model file
    model_path = "/path/to/your/model.gguf"
    
    # Check if model exists
    if not Path(model_path).exists():
        print(f"❌ Model not found: {model_path}")
        print("💡 Please update the model_path variable with the correct path")
        return
    
    print("🚀 AI Room Interactive Chat Example")
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
    
    # Start interactive chat
    interactive_chat(chat)
    
    # Cleanup
    print("\n🧹 Cleaning up...")
    loader.unload_model()
    print("✅ Example completed!")

if __name__ == "__main__":
    main()
