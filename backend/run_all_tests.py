"""
Master Test Runner - Runs all backend tests
"""
import sys
import subprocess
import os

tests = [
    "test_lexers.py",
    "test_parsers.py",
    "test_semantic.py",
    "test_ir_utils.py",
    "test_codegen.py"  
]

def run_test(test_file):
    print(f"\n{'='*60}")
    print(f"RUNNING: {test_file}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(
            [sys.executable, test_file],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
            
        if result.returncode == 0:
            print(f"[PASS] {test_file}")
            return True
        else:
            print(f"[FAIL] {test_file} (Exit code: {result.returncode})")
            return False
            
    except Exception as e:
        print(f"[ERROR] Could not run {test_file}: {e}")
        return False

if __name__ == "__main__":
    print("\nSYNTAXSHIFT BACKEND - TEST SUITE")
    print("================================")
    
    passed = 0
    failed = 0
    
    for test in tests:
        if run_test(test):
            passed += 1
        else:
            failed += 1
    
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Total Tests: {len(tests)}")
    print(f"Passed:      {passed}")
    print(f"Failed:      {failed}")
    
    if failed == 0:
        print("\n[SUCCESS] ALL TESTS PASSED!")
    else:
        print("\n[FAILURE] SOME TESTS FAILED.")
        sys.exit(1)
