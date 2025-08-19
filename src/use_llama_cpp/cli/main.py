"""
Main CLI entry point for AI Room application.
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import Optional

from ..core.model_loader import ModelLoader
from ..core.chat import AIChat
from ..utils.gpu_checker import GPUChecker


def setup_logging(verbose: bool = False):
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="AI Room - GPU-accelerated AI chat application",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  airoom /path/to/model.gguf                    # Basic usage
  airoom model.gguf --gpu-layers 20            # Use 20 GPU layers
  airoom model.gguf --context-size 4096        # Larger context window
  airoom model.gguf --verbose                   # Verbose logging
  airoom model.gguf --interactive              # Interactive chat mode
        """
    )
    
    parser.add_argument(
        'model_path',
        type=str,
        help='Path to the GGUF model file'
    )
    
    parser.add_argument(
        '--gpu-layers',
        type=int,
        default=-1,
        help='Number of GPU layers to use (-1 for all, 0 for CPU only)'
    )
    
    parser.add_argument(
        '--context-size',
        type=int,
        default=2048,
        help='Context window size'
    )
    
    parser.add_argument(
        '--max-tokens',
        type=int,
        default=100,
        help='Maximum tokens in response'
    )
    
    parser.add_argument(
        '--temperature',
        type=float,
        default=0.3,
        help='Response randomness (0.0 = deterministic, 1.0 = random)'
    )
    
    parser.add_argument(
        '--interactive',
        action='store_true',
        help='Run in interactive chat mode'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    parser.add_argument(
        '--system-prompt',
        type=str,
        default="You are a helpful AI assistant. Keep your responses concise and relevant.",
        help='System prompt for the AI assistant'
    )
    
    return parser.parse_args()


def interactive_chat(chat: AIChat):
    """Run interactive chat mode."""
    print("\n💬 Interactive chat mode (type 'quit', 'exit', or 'q' to exit)")
    print("💡 Type 'reset' to clear conversation history")
    print("💡 Type 'history' to view conversation history")
    print("💡 Type 'help' for available commands")
    
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
                for msg in history[1:]:  # Skip system prompt
                    role = msg['role'].title()
                    content = msg['content'][:100] + "..." if len(msg['content']) > 100 else msg['content']
                    print(f"  {role}: {content}")
                continue
                
            if user_input.lower() == 'help':
                print("\n📖 Available Commands:")
                print("  quit/exit/q - Exit the chat")
                print("  reset - Clear conversation history")
                print("  history - View conversation history")
                print("  help - Show this help message")
                continue
            
            # Get AI response
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
    """Main entry point."""
    args = parse_arguments()
    setup_logging(args.verbose)
    
    logger = logging.getLogger(__name__)
    
    # Check GPU availability
    print("🔍 Checking GPU availability...")
    GPUChecker.print_gpu_summary()
    
    # Initialize model loader
    model_loader = ModelLoader(
        model_path=args.model_path,
        gpu_layers=args.gpu_layers,
        context_size=args.context_size
    )
    
    # Load model
    print(f"\n🚀 Loading model: {args.model_path}")
    model = model_loader.load_model()
    
    if not model:
        logger.error("Failed to load model")
        sys.exit(1)
    
    # Initialize chat
    chat = AIChat(model, system_prompt=args.system_prompt)
    
    if args.interactive:
        interactive_chat(chat)
    else:
        # Simple test
        print("\n🧪 Testing model with a simple prompt...")
        response = chat.get_response("Hello! How are you today?")
        if response:
            print(f"Response: {response}")
        else:
            print("Failed to get response")
    
    # Cleanup
    model_loader.unload_model()


if __name__ == "__main__":
    main()
