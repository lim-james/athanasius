import unittest
from unittest.mock import patch
from io import StringIO
import os
from cli import main
import json

class TestCLITool(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_file.txt"
        with open(self.test_file, "w") as f:
            f.write("This is a test file.")

        self.test_list_folder_path = "test_list_folder"
        os.mkdir(self.test_list_folder_path)
        with open(os.path.join(self.test_list_folder_path, "file_in_folder.txt"), "w") as f:
            f.write("File in folder")

        self.archive_file = "archive.ath"
        self.test_archive_folder_path = "test_archive_folder"
        os.mkdir(self.test_archive_folder_path)
        self.test_archive_subfolder_path = os.path.join(self.test_archive_folder_path, "subfolder")
        os.mkdir(self.test_archive_subfolder_path)
        with open(os.path.join(self.test_archive_folder_path, "file1.txt"), "w") as f:
            f.write("File 1 Content")
        with open(os.path.join(self.test_archive_folder_path, "file2.txt"), "w") as f:
            f.write("File 2 Content")
        with open(os.path.join(self.test_archive_subfolder_path, "file3.txt"), "w") as f:
            f.write("File 3 Content")

        self.restored_folder = "folder"

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        
        def remove_dir(dir_path):
            for item in os.listdir(dir_path):
                item_path = os.path.join(dir_path, item)
                if os.path.isdir(item_path):
                    remove_dir(item_path) 
                elif os.path.isfile(item_path):
                    os.remove(item_path)
            os.rmdir(dir_path)
            
        if os.path.exists(self.test_list_folder_path):
            remove_dir(self.test_list_folder_path)

        if os.path.exists(self.test_archive_folder_path):
            remove_dir(self.test_archive_folder_path)
        if os.path.exists(self.archive_file):
            os.remove(self.archive_file)

        if os.path.exists(self.restored_folder):
            remove_dir(self.restored_folder)

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
            self.assertIn("file2.txt", content)
            self.assertIn("subfolder", content)
            self.assertIn("file3.txt", content["subfolder"])
            self.assertEqual(content["file1.txt"], "File 1 Content")
            self.assertEqual(content["subfolder"]["file3.txt"], "File 3 Content")

    @patch("sys.stdout", new_callable=StringIO)
    def test_archive_and_extract(self, mock_stdout):
        archive_name = "archive.ath"
        with patch("sys.argv", ["cli.py", "archive", "test_archive_folder"]):
            main()
        
        self.assertTrue(os.path.exists(archive_name))

        with patch("sys.argv", ["cli.py", "extract", archive_name]):
            main()

        self.assertTrue(os.path.exists(self.restored_folder))
        self.assertTrue(os.path.exists(os.path.join(self.restored_folder, "file1.txt")))
        self.assertTrue(os.path.exists(os.path.join(self.restored_folder, "file2.txt")))

        subfolder_path = os.path.join(self.restored_folder, "subfolder")
        self.assertTrue(os.path.exists(subfolder_path))
        self.assertTrue(os.path.exists(os.path.join(subfolder_path, "file3.txt")))

        with open(os.path.join(self.restored_folder, "file1.txt"), "r") as file:
            self.assertEqual(file.read(), "File 1 Content")
        with open(os.path.join(self.restored_folder, "file2.txt"), "r") as file:
            self.assertEqual(file.read(), "File 2 Content")
        with open(os.path.join(subfolder_path, "file3.txt"), "r") as file:
            self.assertEqual(file.read(), "File 3 Content")

if __name__ == "__main__":
    unittest.main()