import unittest
from unittest.mock import patch
from io import StringIO
import os
from cli import main
import json

class TestCLITool(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_file.txt"
        self.test_list_folder_path = "test_list_folder"
        self.archive_file = "archive.ath"
        self.test_archive_folder_path = "test_archive_folder"
        os.mkdir(self.test_list_folder_path)
        os.mkdir(self.test_archive_folder_path)
        with open(self.test_file, "w") as f:
            f.write("This is a test file.")
        with open(os.path.join(self.test_list_folder_path, "file_in_folder.txt"), "w") as f:
            f.write("File in folder")
        with open(os.path.join(self.test_archive_folder_path, "file1.txt"), "w") as f:
            f.write("File 1 Content")
        with open(os.path.join(self.test_archive_folder_path, "file2.txt"), "w") as f:
            f.write("File 2 Content")

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        if os.path.exists(self.test_list_folder_path):
            for item in os.listdir(self.test_list_folder_path):
                os.remove(os.path.join(self.test_list_folder_path, item))
            os.rmdir(self.test_list_folder_path)
        if os.path.exists(self.test_archive_folder_path):
            for item in os.listdir(self.test_archive_folder_path):
                os.remove(os.path.join(self.test_archive_folder_path, item))
            os.rmdir(self.test_archive_folder_path)
        if os.path.exists(self.archive_file):
            os.remove(self.archive_file)

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
    @patch("sys.argv", new=["cli.py", "list", "test_list_folder"])
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

    @patch("sys.stdout", new_callable=StringIO)
    @patch("sys.argv", new=["cli.py", "archive", "test_archive_folder"])
    def test_archive_folder(self, mock_stdout):
        main()
        self.assertTrue(os.path.exists(self.archive_file))

        with open(self.archive_file, "r") as archive:
            content = json.load(archive)
            self.assertIn("file1.txt", content)
            self.assertEqual(content["file1.txt"], "File 1 Content")


if __name__ == "__main__":
    unittest.main()