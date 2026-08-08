#! /usr/bin/python3
'''
Project started mid Germinal 2003:
PReFScript: A Partial Recursive Functions Lab

Module version mid Thermidor 2026:
prefscript.py: temporary main program

Author: Jose L Balcazar, ORCID 0000-0003-4248-4528, april 2023 onwards 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)
'''


__version__ = "2.0"

from parser import prfsparser, ScriptMaker
from script import PReFScript

import subprocess
from pathlib import Path

TEST_DIR = Path("../tests_v2")
INTERPRETER = "./prefscript.py"

# NOT COUNTING the files in folder err
expected_outputs = (39, 3, 3, 0, 2, 1521, 6, 43, 49, 38, 1, 2, 16, 1521, 0, 43, 0, 3) 

def run_tests():
    test_files = sorted(TEST_DIR.glob("*.2prfs"))
    print(f"{len(test_files)} files found in {TEST_DIR}.")
    passed = 0

    for test_path, expected in zip(test_files, expected_outputs):
        # ~ print(f"Test of {test_path}...\n")
        result = subprocess.run(
            [INTERPRETER, str(test_path)],
            input="39\n\n",
            capture_output=True,
            text=True
        )

        # Check execution status
        if result.returncode == 0 and result.stdout.strip() == str(expected):
            passed += 1
        else:
            print(f"[FAIL] {test_path}")
            print(f"Error output: {result.stderr.strip()}, expected: {expected}.")
            break
    print(f"{passed} passed.")


if __name__ == "__main__":
    run_tests()
