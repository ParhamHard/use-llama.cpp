#!/usr/bin/env python3
"""
Test script to verify CUDA functionality with llama.cpp
"""

import os
import sys
import ctypes

def test_cuda_libraries():
    """Test if the CUDA libraries can be loaded directly"""
    
    # Set library path to use system libraries
    os.environ['LD_LIBRARY_PATH'] = '/usr/lib/x86_64-linux-gnu:/usr/lib'
    
    # Try to load the CUDA library directly
    try:
        cuda_lib = ctypes.CDLL('/home/parhamhard/projects/use llama/llama-cpp-python/llama_cpp/lib/libggml-cuda.so')
        print("✓ Successfully loaded libggml-cuda.so")
        return True
    except Exception as e:
        print(f"✗ Failed to load libggml-cuda.so: {e}")
        return False

def test_llama_library():
    """Test if the llama library can be loaded directly"""
    
    # Set library path to use system libraries
    os.environ['LD_LIBRARY_PATH'] = '/usr/lib/x86_64-linux-gnu:/usr/lib'
    
    # Try to load the llama library directly
    try:
        llama_lib = ctypes.CDLL('/home/parhamhard/projects/use llama/llama-cpp-python/llama_cpp/lib/libllama.so')
        print("✓ Successfully loaded libllama.so")
        return True
    except Exception as e:
        print(f"✗ Failed to load libllama.so: {e}")
        return False

def test_python_import():
    """Test if we can import llama_cpp with proper library paths"""
    
    # Set library path to use system libraries
    os.environ['LD_LIBRARY_PATH'] = '/usr/lib/x86_64-linux-gnu:/usr/lib'
    
    try:
        import llama_cpp
        print(f"✓ Successfully imported llama_cpp version: {llama_cpp.__version__}")
        
        # Check for CUDA support
        if hasattr(llama_cpp, '_lib'):
            lib_str = str(llama_cpp._lib)
            if 'cuda' in lib_str.lower():
                print("✓ CUDA support detected in llama_cpp")
                return True
            else:
                print("✗ No CUDA support detected in llama_cpp")
                return False
        else:
            print("✗ No _lib attribute found in llama_cpp")
            return False
            
    except Exception as e:
        print(f"✗ Failed to import llama_cpp: {e}")
        return False

if __name__ == "__main__":
    print("Testing CUDA setup for llama.cpp...")
    print("=" * 50)
    
    # Test 1: Load CUDA library directly
    print("\n1. Testing CUDA library loading:")
    cuda_ok = test_cuda_libraries()
    
    # Test 2: Load llama library directly
    print("\n2. Testing llama library loading:")
    llama_ok = test_llama_library()
    
    # Test 3: Test Python import
    print("\n3. Testing Python import:")
    python_ok = test_python_import()
    
    print("\n" + "=" * 50)
    if cuda_ok and llama_ok and python_ok:
        print("🎉 All tests passed! Your CUDA setup is working correctly.")
    else:
        print("❌ Some tests failed. Check the output above for details.")
