from llama_cpp import Llama
import os
import sys
import torch

# Configuration
MODEL_PATH = r"/home/parhamhard/projects/llm-web/text-generation-webui/user_data/models/TheBloke/dolphin-2_6-phi-2-GGUF/dolphin-2_6-phi-2.Q4_K_M.gguf"
GPU_LAYERS = -1  # -1 = all layers on GPU, 0 = CPU only
CONTEXT_SIZE = 2048
MAX_TOKENS = 256
TEMPERATURE = 0.7


def validate_model_path(model_path):
    """Validate that the model file exists and is accessible"""
    if not os.path.exists(model_path):
        print(f"❌ Model file not found: {model_path}")
        print("💡 Please check the MODEL_PATH configuration in main.py")
        print("💡 Make sure the path is correct and the file exists")
        return False
    
    if not model_path.endswith('.gguf'):
        print(f"⚠️  Warning: Model file doesn't have .gguf extension: {model_path}")
        print("💡 This might not be a valid GGUF model file")
    
    file_size = os.path.getsize(model_path) / (1024 * 1024 * 1024)  # Size in GB
    print(f"📁 Model file found: {os.path.basename(model_path)}")
    print(f"📏 File size: {file_size:.2f} GB")
    
    return True

def check_gpu_availability():
    """Check if GPU is available and provide information"""
    print("🔍 Checking GPU availability...")
    
    # Check CUDA availability
    if torch.cuda.is_available():
        gpu_count = torch.cuda.device_count()
        print(f"✅ CUDA is available! Found {gpu_count} GPU(s)")
        
        for i in range(gpu_count):
            gpu_name = torch.cuda.get_device_name(i)
            gpu_memory = torch.cuda.get_device_properties(i).total_memory / (1024**3)
            print(f"   GPU {i}: {gpu_name} ({gpu_memory:.1f} GB)")
        
        # Set default GPU device
        torch.cuda.set_device(0)
        print(f"🎯 Using GPU device: {torch.cuda.current_device()}")
        return True
    else:
        print("❌ CUDA is not available")
        print("💡 Make sure you have:")
        print("   - NVIDIA GPU drivers installed")
        print("   - CUDA toolkit installed")
        print("   - PyTorch with CUDA support")
        print("   - llama-cpp-python compiled with GPU support")
        return False

def load_model(model_path, gpu_layers=-1, context_size=2048):
    """Load a GGUF model with GPU acceleration"""
    if not os.path.exists(model_path):
        print(f"❌ Model not found: {model_path}")
        return None
    
    print(f"🚀 Loading model: {os.path.basename(model_path)}")
    print(f"📍 Path: {model_path}")
    print(f"🎮 GPU layers: {gpu_layers}")
    print(f"📝 Context size: {context_size}")
    
    try:
        # Force GPU usage with simplified parameters
        llm = Llama(
            model_path=model_path,
            n_gpu_layers=gpu_layers,  # -1 = all layers on GPU
            n_ctx=context_size,
            n_batch=512,
            verbose=False,  # Changed to False to reduce debug output
            # Explicit GPU configuration
            offload_kqv=True,  # Offload key/query/value to GPU
            mul_mat_q=True,    # Use GPU for matrix multiplication
            # Remove potentially conflicting parameters
        )
        print("✅ Model loaded successfully!")
        
        # Verify GPU usage
        if gpu_layers > 0:
            print(f"🎮 Model configured to use {gpu_layers} GPU layers")
        elif gpu_layers == -1:
            print("🎮 Model configured to use ALL layers on GPU")
        else:
            print("⚠️  Model configured for CPU-only usage")
            
        return llm
    except Exception as e:
        print(f"❌ Failed to load model: {e}")
        print("💡 This might be due to:")
        print("   - GPU memory limitations")
        print("   - llama-cpp-python not compiled with GPU support")
        print("   - CUDA version compatibility issues")
        return None

def chat_with_model(llm, prompt, max_tokens=256, temperature=0.7):
    """Chat with the loaded model"""
    if not llm:
        print("❌ No model loaded!")
        return
    
    print(f"\n💬 You: {prompt}")
    print("🤖 AI: ", end="", flush=True)
    
    try:
        # Use create_chat_completion since this model has a chat template
        messages = [{"role": "user", "content": prompt}]
        response = llm.create_chat_completion(
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            stop=["User:", "\n\n", "<|im_end|>"],
            stream=False
        )
        
        if response and 'choices' in response and len(response['choices']) > 0:
            choice = response['choices'][0]
            
            # Handle both text completion and chat completion formats
            ai_response = None
            if 'text' in choice:
                # Text completion format
                ai_response = choice['text'].strip()
            elif 'message' in choice and 'content' in choice['message']:
                # Chat completion format
                ai_response = choice['message']['content'].strip()
            
            if ai_response:
                # Clean the response by removing any debug/timing information
                # Split by newlines and take only the first meaningful line
                lines = ai_response.split('\n')
                clean_response = ""
                for line in lines:
                    line = line.strip()
                    # Skip lines that look like debug output
                    if (line and 
                        not line.startswith('llama_print_timings:') and
                        not line.startswith('llama_') and
                        not line.startswith('>') and
                        not line.startswith('✅') and
                        not line.startswith('💬') and
                        not line.startswith('🤖')):
                        clean_response = line
                        break
                
                if clean_response:
                    print(clean_response)
                    return clean_response
                else:
                    print(ai_response)  # Fallback to original response
                    return ai_response
            else:
                print("❌ Empty response text")
                return None
        else:
            print("❌ No response generated")
            return None
            
    except Exception as e:
        print(f"❌ Error generating response: {e}")
        return None


def main():
    """Main function to run the chat application"""
    print("🚀 AI Chat Assistant - Starting up...")
    
    # Check GPU availability first
    gpu_available = check_gpu_availability()
    
    if not gpu_available:
        print("⚠️  GPU not available, but continuing with CPU fallback...")
        print("💡 Performance will be slower on CPU")
    
    # Validate model path first
    if not validate_model_path(MODEL_PATH):
        print("❌ Cannot proceed without a valid model file. Exiting.")
        return

    # Load the model
    llm = load_model(MODEL_PATH, GPU_LAYERS, CONTEXT_SIZE)
    
    if not llm:
        print("❌ Failed to load model. Exiting.")
        return

    print("\n🤖 AI Chat Assistant Ready!")
    print("💡 Type 'quit' or 'exit' to end the conversation")
    print("💡 Type 'clear' to start a new conversation")
    print("-" * 50)

    # Interactive chat loop
    conversation_history = []
    
    while True:
        try:
            # Get user input
            user_input = input("\n💬 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            elif user_input.lower() in ['clear', 'reset']:
                conversation_history = []
                print("🧹 Conversation history cleared!")
                continue
            elif not user_input:
                continue
            
            # Add user message to history
            conversation_history.append({"role": "user", "content": user_input})
            
            # Get response from model
            response = chat_with_model(llm, user_input, MAX_TOKENS, TEMPERATURE)
            
            if response:
                # Add AI response to history
                conversation_history.append({"role": "assistant", "content": response})
                # Remove the redundant character count since the response is already displayed
            else:
                print("\n❌ No response received")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
