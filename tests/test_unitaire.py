import unittest
from app.main import main
import io
import sys
from app.main import get_random_message

class TestMain(unittest.TestCase):
    def test_hey_output(self):
        original_stdout = sys.stdout
        sys.stdout = io.StringIO()  
        main() 
        output = sys.stdout.getvalue()
        output = sys.stdout.getvalue().strip().split('\n')[0]
        self.assertEqual(output, "Hey you!")

    def test_random_message_output(self):
        messages = ["Keep it up :)", "You got this :)", "You're almost at the finish line :)", "It will be okay :)"]
        result = get_random_message()
        self.assertIn(result, messages)



