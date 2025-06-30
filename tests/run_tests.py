import pytest

if __name__ == "__main__":

    pytest.main([
        "tests/test_create_task.py",
        "-v",  # enable verbose mode to display more information about test cases
        "--tb=short"  # Shorter traceback format to display the essential error information

    ])