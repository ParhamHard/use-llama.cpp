#!/usr/bin/env python3
"""
Test script to verify all dependencies are working correctly
"""

def test_imports():
    """Test all critical imports"""
    print("🔍 Testing imports...")
    
    try:
        import numpy
        print(f"✅ numpy: {numpy.__version__}")
    except ImportError as e:
        print(f"❌ numpy import failed: {e}")
        return False
    
    try:
        import torch
        print(f"✅ torch: {torch.__version__}")
        print(f"   CUDA available: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"   CUDA version: {torch.version.cuda}")
            print(f"   GPU count: {torch.cuda.device_count()}")
    except ImportError as e:
        print(f"❌ torch import failed: {e}")
        return False
    
    try:
        from llama_cpp import Llama
        print("✅ llama_cpp import successful")
    except ImportError as e:
        print(f"❌ llama_cpp import failed: {e}")
        return False
    
    return True

def test_main_module():
    """Test importing the main module"""
    print("\n🔍 Testing main module...")
    
    try:
        import main
        print("✅ main module imported successfully")
        
        # Test if key functions exist
        if hasattr(main, 'check_gpu_availability'):
            print("✅ check_gpu_availability function found")
        if hasattr(main, 'load_model'):
            print("✅ load_model function found")
        if hasattr(main, 'chat_with_model'):
            print("✅ chat_with_model function found")
            
    except ImportError as e:
        print(f"❌ main module import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ main module error: {e}")
        return False
    
    return True

def main():
    """Run all tests"""
    print("🚀 Dependency Test Suite")
    print("=" * 40)
    
    # Test imports
    imports_ok = test_imports()
    
    # Test main module
    main_ok = test_main_module()
    
    print("\n" + "=" * 40)
    if imports_ok and main_ok:
        print("🎉 All tests passed! Your environment is ready.")
        print("💡 You can now run: python main.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
    
    return imports_ok and main_ok

if __name__ == "__main__":
    main()
