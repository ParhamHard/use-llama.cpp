#!/usr/bin/env python3
"""
Script to load dolphin-2.6-phi-2 model using llama.cpp with GPU acceleration
"""

import os
from llama_cpp import Llama

def main():
    # Model path
    model_path = "/home/parhamhard/projects/llm-web/text-generation-webui/user_data/models/TheBloke/dolphin-2_6-phi-2-GGUF/dolphin-2_6-phi-2.Q4_K_M.gguf"
    
    print(f"Loading model: {model_path}")
    print("Using GPU acceleration...")
    
    try:
        # Load model with GPU acceleration
        llm = Llama(
            model_path=model_path,
            n_gpu_layers=-1,  # Use all available GPU layers
            n_ctx=2048,       # Context window size
            n_batch=512,      # Batch size for processing
            verbose=False,     # Show loading progress
            chat_format="chatml"  # Use ChatML format for better responses
        )
        
        print("✅ Model loaded successfully with GPU acceleration!")
        print("Model loaded with GPU layers enabled")
        
        # Test the model with a simple prompt
        print("\n🧪 Testing model with a simple prompt...")
        
        messages = [
            {"role": "system", "content": "You are a helpful AI assistant. Keep your responses concise and relevant."},
            {"role": "user", "content": "Hello! How are you today?"}
        ]
        
        print(f"Prompt: Hello! How are you today?")
        
        response = llm.create_chat_completion(
            messages=messages,
            max_tokens=50,      # Limit response length
            temperature=0.1,    # Lower temperature for more focused responses
            top_p=0.9,         # Nucleus sampling
            top_k=40,          # Top-k sampling
            repeat_penalty=1.1, # Prevent repetition
            stop=["\n", "Human:", "Assistant:"]
        )
        
        response_text = response['choices'][0]['message']['content'].strip()
        print(f"Response: {response_text}")
        
        # Interactive mode
        print("\n💬 Entering interactive mode (type 'quit' to exit):")
        
        # Initialize conversation history
        conversation = [
            {"role": "system", "content": "You are a helpful AI assistant. Keep your responses concise and relevant. Don't generate code unless specifically asked."}
        ]
        
        while True:
            user_input = input("\nYou: ")
            if user_input.lower() in ['quit', 'exit', 'q']:
                break
                
            # Add user message to conversation
            conversation.append({"role": "user", "content": user_input})
            
            try:
                response = llm.create_chat_completion(
                    messages=conversation,
                    max_tokens=100,     # Limit response length
                    temperature=0.3,    # Lower temperature for more coherent responses
                    top_p=0.9,         # Nucleus sampling
                    top_k=40,          # Top-k sampling
                    repeat_penalty=1.1, # Prevent repetition
                    stop=["\nHuman:", "Human:", "Assistant:"]
                )
                
                response_text = response['choices'][0]['message']['content'].strip()
                if response_text:
                    print(f"Assistant: {response_text}")
                    # Add assistant response to conversation
                    conversation.append({"role": "assistant", "content": response_text})
                else:
                    print("Assistant: I'm not sure how to respond to that.")
                    
            except Exception as e:
                print(f"Error generating response: {e}")
                print("Assistant: I encountered an error. Please try again.")
            
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
