import unittest
from app.main import main
import io
import sys

class TestMain(unittest.TestCase):
    def test_output(self):
        original_stdout = sys.stdout
        sys.stdout = io.StringIO()  
        main() 
        output = sys.stdout.getvalue()
        sys.stdout = original_stdout
        self.assertEqual(output.strip(), "Hey you!")

