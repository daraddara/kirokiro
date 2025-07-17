"""
Run all tests for the Puyo Puyo Puzzle Game
"""

import os
import sys
import subprocess
import glob

def run_test_file(test_file):
    """
    Run a single test file
    """
    print(f"\n=== Running tests from {test_file} ===")
    
    # Run the test file as a separate process
    result = subprocess.run(['python', test_file], capture_output=True, text=True)
    
    # Print the output
    print(result.stdout)
    
    if result.returncode != 0:
        print(f"ERROR: Test file {test_file} failed with return code {result.returncode}")
        print(result.stderr)
        return False
    
    return True

def run_all_tests():
    """
    Run all test files in the tests directory
    """
    print("=== Running All Tests ===")
    
    # Find all test files
    test_files = glob.glob('tests/test_*.py')
    
    if not test_files:
        print("No test files found!")
        return
    
    # Sort test files for consistent execution order
    test_files.sort()
    
    # Run each test file
    all_passed = True
    for test_file in test_files:
        if not run_test_file(test_file):
            all_passed = False
    
    if all_passed:
        print("\n=== All Tests Passed! ===")
    else:
        print("\n=== Some Tests Failed! ===")

if __name__ == "__main__":
    run_all_tests()