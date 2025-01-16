import unittest
from unittest.mock import patch
from io import StringIO
import os
from cli import main

class TestCLITool(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_file.txt"
        self.test_folder = "test_folder"
        os.mkdir(self.test_folder)
        with open(self.test_file, "w") as f:
            f.write("This is a test file.")
        with open(os.path.join(self.test_folder, "file_in_folder.txt"), "w") as f:
            f.write("File in folder")

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        if os.path.exists(self.test_folder):
            for item in os.listdir(self.test_folder):
                os.remove(os.path.join(self.test_folder, item))
            os.rmdir(self.test_folder)

    @patch("sys.stdout", new_callable=StringIO)
    @patch("sys.argv", new=["cli.py", "read", "test_file.txt"])
    def test_file_content(self, mock_stdout):
        main()
        output = mock_stdout.getvalue()
        self.assertIn("This is a test file.", output)

    @patch("sys.stdout", new_callable=StringIO)
    @patch("sys.argv", new=["cli.py", "read", "nonexistent.txt"])
    def test_file_not_found(self, mock_stdout):
        main()
        output = mock_stdout.getvalue()
        self.assertIn("Error: The file 'nonexistent.txt' does not exists.", output)

    @patch("sys.stdout", new_callable=StringIO)
    @patch("sys.argv", new=["cli.py", "list", "test_folder"])
    def test_list_folder(self, mock_stdout):
        main()
        output = mock_stdout.getvalue()
        self.assertIn("📄 file_in_folder.txt", output)

    @patch("sys.stdout", new_callable=StringIO)
    @patch("sys.argv", new=["cli.py", "list", "nonexistent_folder"])
    def test_folder_not_found(self, mock_stdout):
        main()
        output = mock_stdout.getvalue()
        self.assertIn("Error: The folder 'nonexistent_folder' does not exist.", output)

if __name__ == "__main__":
    unittest.main()