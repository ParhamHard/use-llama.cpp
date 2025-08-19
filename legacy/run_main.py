#!/usr/bin/env python3
"""
Wrapper script to fix library path issues and run main.py
"""

import os
import sys
import subprocess

def fix_library_path():
    """Fix the library path to use system libraries instead of conda ones"""
    
    # Get the current environment
    env = os.environ.copy()
    
    # Set library path to use system libraries first
    system_lib_path = "/usr/lib/x86_64-linux-gnu:/usr/lib"
    
    if 'LD_LIBRARY_PATH' in env:
        env['LD_LIBRARY_PATH'] = f"{system_lib_path}:{env['LD_LIBRARY_PATH']}"
    else:
        env['LD_LIBRARY_PATH'] = system_lib_path
    
    # Also set LIBRARY_PATH for linking
    if 'LIBRARY_PATH' in env:
        env['LIBRARY_PATH'] = f"{system_lib_path}:{env['LIBRARY_PATH']}"
    else:
        env['LIBRARY_PATH'] = system_lib_path
    
    print("🔧 Fixed library paths:")
    print(f"   LD_LIBRARY_PATH: {env['LD_LIBRARY_PATH']}")
    print(f"   LIBRARY_PATH: {env['LIBRARY_PATH']}")
    
    return env

def main():
    """Main function to run main.py with fixed library paths"""
    
    print("🚀 Starting AI Chat Assistant with library path fixes...")
    print("=" * 60)
    
    # Fix library paths
    env = fix_library_path()
    
    # Check if main.py exists
    if not os.path.exists('main.py'):
        print("❌ main.py not found!")
        return
    
    # Try to import llama_cpp to test if it works
    try:
        import llama_cpp
        print("✅ llama_cpp module imported successfully!")
        print(f"   Version: {llama_cpp.__version__}")
        
        # Check CUDA support
        if hasattr(llama_cpp, '_lib'):
            print(f"   Library info: {llama_cpp._lib}")
        else:
            print("   Library info: Not available")
            
    except Exception as e:
        print(f"❌ Failed to import llama_cpp: {e}")
        print("\n💡 This indicates the library path issue is still present.")
        print("💡 You may need to:")
        print("   1. Deactivate conda: conda deactivate")
        print("   2. Use system Python: /usr/bin/python3")
        print("   3. Or fix the conda environment library versions")
        return
    
    print("\n🎯 Running main.py...")
    print("-" * 40)
    
    # Run main.py
    try:
        # Import and run main.py directly
        import main
        print("✅ main.py executed successfully!")
        
    except Exception as e:
        print(f"❌ Error running main.py: {e}")
        print("\n💡 The library path fix worked, but there's another issue.")
        print("💡 Check the error details above.")

if __name__ == "__main__":
    main()
