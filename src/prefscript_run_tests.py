# Code by Gemini

import subprocess
from pathlib import Path

# Path to your executable interpreter script
INTERPRETER = "./main.py"  # Ensure it has executable permissions (+x)

def run_test(source_code: str):
    result = subprocess.run(
        [INTERPRETER],          # Called directly without 'python3'
        input=source_code,      # Feeds string directly into stdin (like cat file | interpreter)
        capture_output=True,
        text=True
    )
    
    return result.stdout, result.stderr, result.returncode

# Example usage:
code = """
def double(x) = x + x
print(double(21))
"""

stdout, stderr, code = run_test(code)
print("Output:", stdout)


'''
earlier code:

import subprocess
from pathlib import Path

# 1. Directory containing your PReFScript test files
TEST_DIR = Path("./tests")
INTERPRETER_SCRIPT = "main.py"  # Path to your interpreter's main entry point

def run_tests():
    # Discover all test files (e.g., .pref or .prefscript)
    test_files = sorted(TEST_DIR.glob("*.pref"))
    
    if not test_files:
        print(f"No test files found in {TEST_DIR.resolve()}")
        return

    passed = 0
    failed = 0

    print(f"Running {len(test_files)} tests...\n" + "-" * 40)

    for test_path in test_files:
        # Call your interpreter as a subprocess
        result = subprocess.run(
            ["python3", INTERPRETER_SCRIPT, str(test_path)],
            capture_output=True,
            text=True
        )

        # Check execution status
        if result.returncode == 0:
            print(f"[PASS] {test_path.name}")
            passed += 1
        else:
            print(f"[FAIL] {test_path.name}")
            print(f"       Error output: {result.stderr.strip()}")
            failed += 1

    print("-" * 40)
    print(f"Summary: {passed} passed, {failed} failed out of {len(test_files)}.")

if __name__ == "__main__":
    run_tests()

'''
