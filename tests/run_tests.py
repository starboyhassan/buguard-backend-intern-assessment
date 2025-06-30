import pytest
import sys
import os

if __name__ == "__main__":

    # Add parent directory to path
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

    pytest.main([
        "tests/test_create_task.py",
        "tests/test_get_tasks.py",
        "-v",  # enable verbose mode to display more information about test cases
        "--tb=short"  # Shorter traceback format to display the essential error information

    ])