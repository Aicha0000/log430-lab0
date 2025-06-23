"""Unit tests for main module."""

import unittest
import io
import sys
from app.main import main, get_random_message

class TestMain(unittest.TestCase):
    """Unit tests for main.py."""
    def test_hey_output(self):
        """Test if the first line of output is 'Hey you!'."""
        original_stdout = sys.stdout
        sys.stdout = io.StringIO()
        try:
            main()
            output = sys.stdout.getvalue().strip().split('\n')[0]
            self.assertEqual(output, "Hey you!")
        finally:
            sys.stdout = original_stdout

    def test_random_message_output(self):
        """Test if the random message is one of the expected messages."""
        messages = [
            "Keep it up :)",
            "You got this :)",
            "You're almost at the finish line :)",
            "It will be okay :)"
        ]
        result = get_random_message()
        self.assertIn(result, messages)
        