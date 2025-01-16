import unittest
from unittest.mock import patch
from io import StringIO
import os
from cli import main

class TestCLITool(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_file.txt"
        with open(self.test_file, "w") as f:
            f.write("This is a test file.")

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    @patch("sys.stdout", new_callable=StringIO)
    @patch("sys.argv", new=["cli.py", "test_file.txt"])
    def test_file_content(self, mock_stdout):
        main()
        output = mock_stdout.getvalue()
        self.assertIn("This is a test file.", output)

    @patch("sys.stdout", new_callable=StringIO)
    @patch("sys.argv", new=["cli.py", "nonexistent.txt"])
    def test_file_not_found(self, mock_stdout):
        main()
        output = mock_stdout.getvalue()
        self.assertIn("Error: The file 'nonexistent.txt' does not exists.", output)

if __name__ == "__main__":
    unittest.main()