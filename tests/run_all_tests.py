import unittest
import os
import sys

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# ANSI colors for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'


def run_test_suite(test_files):
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    for test_file in test_files:
        try:
            # Construct the module name from the file name
            module_name = f"tests.{os.path.splitext(test_file)[0]}"
            tests = loader.loadTestsFromName(module_name)
            suite.addTests(tests)
        except ImportError as e:
            print(f"{RED}Error importing {test_file}: {e}{RESET}")

    runner = unittest.TextTestRunner(verbosity=0)
    result = runner.run(suite)

    return result


if __name__ == "__main__":
    test_files = [
        "test_anomaly_detector.py",
        "test_data_stream.py",
        "test_stream_processor.py",
        "test_visualizer.py"
    ]

    print(f"{YELLOW}Running all tests...{RESET}")
    result = run_test_suite(test_files)

    if result.wasSuccessful():
        print(f"{GREEN}All tests passed successfully!{RESET}")
        sys.exit(0)
    else:
        print(f"{RED}Some tests failed.{RESET}")
        sys.exit(1)
