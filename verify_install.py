#!/usr/bin/env python3
"""
PhonoCrypt Installation Verification Script
===========================================

Run this script to verify that PhonoCrypt is installed and working correctly.
"""

import sys
import os

def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)

def print_success(text):
    """Print success message."""
    print(f"✅ {text}")

def print_error(text):
    """Print error message."""
    print(f"❌ {text}")

def print_info(text):
    """Print info message."""
    print(f"ℹ️  {text}")
     
def verify_python_version():
    """Verify Python version."""
    print_header("Python Version Check")
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print_success("Python version is 3.8 or higher")
        return True
    else:
        print_error("Python 3.8 or higher required")
        return False

def verify_espeak():
    """Verify espeak-ng installation."""
    print_header("espeak-ng Installation Check")
    
    # Check for environment variable
    lib_path = os.environ.get('PHONEMIZER_ESPEAK_LIBRARY')
    if lib_path:
        print_info(f"PHONEMIZER_ESPEAK_LIBRARY set to: {lib_path}")
    
    # Try to find espeak-ng library
    common_paths = [
        '/opt/homebrew/lib/libespeak-ng.dylib',
        '/usr/local/lib/libespeak-ng.dylib',
        '/usr/lib/x86_64-linux-gnu/libespeak-ng.so',
        '/usr/lib/libespeak-ng.so',
    ]
    
    found = False
    for path in common_paths:
        if os.path.exists(path):
            print_success(f"Found espeak-ng library at: {path}")
            found = True
            break
    
    if not found:
        print_error("espeak-ng library not found")
        print_info("Install with: brew install espeak-ng (macOS)")
        return False
    
    return True

def verify_imports():
    """Verify that core modules can be imported."""
    print_header("Module Import Check")
    
    try:
        import core
        print_success("core package imported")
    except ImportError as e:
        print_error(f"Failed to import core: {e}")
        return False
    
    try:
        from core import PhoneticEngine
        print_success("PhoneticEngine imported")
    except ImportError as e:
        print_error(f"Failed to import PhoneticEngine: {e}")
        return False
    
    try:
        from core import text_to_phonemes, phonemes_to_text
        print_success("Convenience functions imported")
    except ImportError as e:
        print_error(f"Failed to import convenience functions: {e}")
        return False
    
    return True

def verify_dependencies():
    """Verify required dependencies."""
    print_header("Dependency Check")
    
    dependencies = [
        ('phonemizer', '3.2.1'),
        ('epitran', '1.24'),
        ('pandas', '2.2.0'),
        ('numpy', '1.26.4'),
    ]
    
    all_ok = True
    for package, min_version in dependencies:
        try:
            module = __import__(package)
            version = getattr(module, '__version__', 'unknown')
            print_success(f"{package} {version} installed")
        except ImportError:
            print_error(f"{package} not installed")
            all_ok = False
    
    return all_ok

def verify_phonetic_engine():
    """Verify that the phonetic engine works."""
    print_header("Phonetic Engine Functionality Check")
    
    try:
        from core import PhoneticEngine
        
        engine = PhoneticEngine()
        print_success("PhoneticEngine initialized")
        
        # Test text to phonemes
        test_text = "hello"
        phonemes = engine.text_to_phonemes(test_text)
        print_success(f"text_to_phonemes('{test_text}') = {phonemes}")
        
        if not phonemes:
            print_error("No phonemes returned")
            return False
        
        # Test phonemes to text
        reconstructed = engine.phonemes_to_text(phonemes)
        print_success(f"phonemes_to_text({phonemes}) = '{reconstructed}'")
        
        # Test consistency
        phonemes2 = engine.text_to_phonemes(test_text)
        if phonemes == phonemes2:
            print_success("Conversion is consistent")
        else:
            print_error("Conversion is not consistent")
            return False
        
        return True
        
    except Exception as e:
        print_error(f"Phonetic engine test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def verify_backend():
    """Verify which backend is being used."""
    print_header("Backend Detection")
    
    try:
        from core.phonetic_engine import PHONEMIZER_AVAILABLE
        
        if PHONEMIZER_AVAILABLE:
            print_success("phonemizer backend available")
            
            try:
                from phonemizer.backend import EspeakBackend
                backend = EspeakBackend('en-us')
                print_success("espeak-ng backend initialized successfully")
                print_info("Using espeak-ng for high-accuracy IPA conversion")
                return True
            except Exception as e:
                print_error(f"espeak-ng backend failed: {e}")
                print_info("Will use fallback backend")
                return False
        else:
            print_error("phonemizer not available")
            return False
            
    except Exception as e:
        print_error(f"Backend check failed: {e}")
        return False

def run_sample_conversion():
    """Run a sample conversion to demonstrate functionality."""
    print_header("Sample Conversion Demo")
    
    try:
        from core import text_to_phonemes, phonemes_to_text
        
        samples = [
            "Hello world",
            "The quick brown fox",
            "PhonoCrypt"
        ]
        
        for text in samples:
            print(f"\nInput: '{text}'")
            phonemes = text_to_phonemes(text)
            print(f"Phonemes: {phonemes}")
            reconstructed = phonemes_to_text(phonemes)
            print(f"Reconstructed: '{reconstructed}'")
        
        print_success("Sample conversions completed")
        return True
        
    except Exception as e:
        print_error(f"Sample conversion failed: {e}")
        return False

def main():
    """Run all verification checks."""
    print_header("PhonoCrypt Installation Verification")
    print("This script will verify that PhonoCrypt is installed correctly.\n")
    
    results = []
    
    # Run all checks
    results.append(("Python Version", verify_python_version()))
    results.append(("espeak-ng", verify_espeak()))
    results.append(("Dependencies", verify_dependencies()))
    results.append(("Imports", verify_imports()))
    results.append(("Backend", verify_backend()))
    results.append(("Phonetic Engine", verify_phonetic_engine()))
    results.append(("Sample Demo", run_sample_conversion()))
    
    # Summary
    print_header("Verification Summary")
    
    all_passed = True
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 70)
    
    if all_passed:
        print("🎉 All checks passed! PhonoCrypt is ready to use.")
        print("\nNext steps:")
        print("  - Run tests: pytest tests/ -v")
        print("  - Try examples: python core/phonetic_engine.py")
        print("  - Read docs: cat README.md")
        return 0
    else:
        print("⚠️  Some checks failed. Please review the errors above.")
        print("\nCommon solutions:")
        print("  - Install espeak-ng: brew install espeak-ng")
        print("  - Reinstall dependencies: pip install -r requirements.txt")
        print("  - Check Python version: python --version")
        return 1

if __name__ == "__main__":
    sys.exit(main())
