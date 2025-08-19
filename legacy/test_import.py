#!/usr/bin/env python3
"""
Test script to diagnose the llama_cpp import issue
"""

import os
import sys
import ctypes

def check_library_paths():
    """Check current library paths and identify the issue"""
    
    print("🔍 Diagnosing Library Path Issues")
    print("=" * 50)
    
    # Check current library paths
    ld_path = os.environ.get('LD_LIBRARY_PATH', 'Not set')
    lib_path = os.environ.get('LIBRARY_PATH', 'Not set')
    conda_prefix = os.environ.get('CONDA_PREFIX', 'Not set')
    
    print(f"📁 Current LD_LIBRARY_PATH: {ld_path}")
    print(f"📁 Current LIBRARY_PATH: {lib_path}")
    print(f"🐍 CONDA_PREFIX: {conda_prefix}")
    print(f"🐍 Python executable: {sys.executable}")
    print(f"🐍 Python version: {sys.version}")
    
    # Check if we're in a conda environment
    if conda_prefix != 'Not set':
        print(f"⚠️  You are in conda environment: {conda_prefix}")
        
        # Check the problematic library
        conda_libstdc = os.path.join(conda_prefix, 'lib', 'libstdc++.so.6')
        if os.path.exists(conda_libstdc):
            print(f"❌ Found old libstdc++ in conda: {conda_libstdc}")
            
            # Try to check the version
            try:
                result = os.popen(f'strings {conda_libstdc} | grep GLIBCXX').read()
                if result:
                    print("   Available GLIBCXX versions:")
                    for line in result.strip().split('\n'):
                        if line.strip():
                            print(f"     {line.strip()}")
                else:
                    print("   No GLIBCXX versions found")
            except:
                print("   Could not check GLIBCXX versions")
    
    print("\n" + "=" * 50)

def test_direct_library_load():
    """Test loading the library directly with ctypes"""
    
    print("🧪 Testing Direct Library Loading")
    print("=" * 50)
    
    # Set library path to system libraries
    os.environ['LD_LIBRARY_PATH'] = '/usr/lib/x86_64-linux-gnu:/usr/lib'
    
    # Try to load the CUDA library directly
    cuda_lib_path = '/home/parhamhard/projects/use llama/llama-cpp-python/llama_cpp/lib/libggml-cuda.so'
    
    if os.path.exists(cuda_lib_path):
        print(f"📁 Found CUDA library: {cuda_lib_path}")
        
        try:
            # Try to load with system library path
            cuda_lib = ctypes.CDLL(cuda_lib_path)
            print("✅ Successfully loaded CUDA library with system path!")
            
            # Try to get a function pointer
            try:
                cuda_lib.cudaGetDeviceCount
                print("✅ CUDA functions are accessible!")
                return True
            except AttributeError:
                print("⚠️  CUDA library loaded but functions not accessible")
                return False
                
        except Exception as e:
            print(f"❌ Failed to load CUDA library: {e}")
            return False
    else:
        print(f"❌ CUDA library not found: {cuda_lib_path}")
        return False

def provide_solutions():
    """Provide solutions to fix the library path issue"""
    
    print("\n💡 Solutions to Fix Library Path Issue")
    print("=" * 50)
    
    print("1. 🚫 Deactivate conda environment:")
    print("   conda deactivate")
    print("   python main.py")
    
    print("\n2. 🔧 Fix conda environment library versions:")
    print("   conda install -c conda-forge libstdcxx-ng")
    print("   conda update libstdcxx-ng")
    
    print("\n3. 🐍 Use system Python (if available):")
    print("   /usr/bin/python3 main.py")
    
    print("\n4. 📚 Rebuild llama-cpp-python with conda-compatible libraries:")
    print("   conda install -c conda-forge gcc_linux-64 gxx_linux-64")
    print("   CMAKE_ARGS='-DGGML_CUDA=ON' pip install llama-cpp-python")
    
    print("\n5. 🔄 Create new conda environment with newer libraries:")
    print("   conda create -n aivenv_new python=3.10")
    print("   conda activate aivenv_new")
    print("   conda install -c conda-forge libstdcxx-ng")
    print("   pip install llama-cpp-python")

def main():
    """Main function to run all tests"""
    
    print("🚀 Llama.cpp Import Diagnostic Tool")
    print("=" * 60)
    
    # Check library paths
    check_library_paths()
    
    # Test direct library loading
    library_works = test_direct_library_load()
    
    if library_works:
        print("\n✅ Good news! Your CUDA libraries are working correctly.")
        print("   The issue is just with the Python import due to conda environment.")
    else:
        print("\n❌ There are deeper issues with the CUDA libraries.")
    
    # Provide solutions
    provide_solutions()
    
    print("\n🎯 Next Steps:")
    if library_works:
        print("   1. Try solution #1 (deactivate conda)")
        print("   2. Or solution #2 (update conda libraries)")
    else:
        print("   1. Check your CUDA installation")
        print("   2. Rebuild the libraries")
        print("   3. Try solution #4 (rebuild with conda tools)")

if __name__ == "__main__":
    main()
