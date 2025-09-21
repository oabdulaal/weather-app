# run_tests.py - Helper script to run tests
#!/usr/bin/env python3
"""
Helper script to run tests
Usage: python3 run_tests.py
"""
import subprocess
import sys

def run_tests():
    """Run pytest with verbose output"""
    try:
        result = subprocess.run([
            sys.executable, '-m', 'pytest', 
            'tests/', 
            '-v',
            '--tb=short'
        ], capture_output=False, text=True)
        
        return result.returncode
    except Exception as e:
        print(f"Error running tests: {e}")
        return 1

if __name__ == '__main__':
    exit_code = run_tests()
    sys.exit(exit_code)