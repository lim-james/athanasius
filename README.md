# Athanasius

Athanasius is a Python-based Command-Line Interface (CLI) tool for managing files and folders. It supports reading files, listing folder contents, archiving folders (including nested structures), and extracting archived folders back to their original structure. The tool is named after Saint Athanasius, symbolizing strength and resilience in handling complex file operations.

---

## Features

### 1. **Read File Content**
Displays the content of a specified file in the terminal.
- **Command**:
  ```bash
  python cli.py read <file_path>
  ```
- **Example**:
  ```bash
  python cli.py read sample.txt
  ```
  Output:
  ```plaintext
  File Content:
  Hello, Athanasius!
  ```

### 2. **List Folder Contents**
Lists the contents of a specified folder, distinguishing between files and subfolders.
- **Command**:
  ```bash
  python cli.py list <folder_path>
  ```
- **Example**:
  ```bash
  python cli.py list .
  ```
  Output:
  ```plaintext
  Contents of folder '.':
  📁 subfolder/
  📄 file1.txt
  📄 file2.txt
  ```

### 3. **Archive Folder**
Creates an archive of a folder (including nested subfolders) and saves it as a `archive.ath` file. The archive stores both folder structure and file contents.
- **Command**:
  ```bash
  python cli.py archive <folder_path> 
  ```
- **Example**:
  ```bash
  python cli.py archive my_folder 
  ```
  Output:
  ```plaintext
  Folder 'my_folder' archived into 'archive.ath'.
  ```

### 4. **Extract Archive**
Extracts the contents of an archive back into their original folder structure.
- **Command**:
  ```bash
  python cli.py extract <archive_name> --output <output_folder>
  ```
- **Example**:
  ```bash
  python cli.py extract archive.ath --output restored_folder
  ```
  Output:
  ```plaintext
  Archive 'archive.ath' extracted to 'restored_folder'.
  ```

---

## Getting Started

### Prerequisites
- Python 3.7 or higher

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/lim-james/athanasius.git
   ```
2. Navigate to the project directory:
   ```bash
   cd athanasius
   ```

### Usage
Run the `cli.py` file with the appropriate commands listed in the **Features** section.

---

## Testing
The project uses Python’s built-in `unittest` framework for testing. To run the tests:
```bash
python -m unittest test_cli.py
```

---

## Roadmap
Planned features for future releases:
1. **Compression**: Integrate file compression using Huffman encoding.
2. **Metadata Support**: Store additional information like timestamps and file sizes in the archive.
3. **Validation**: Ensure archive integrity during extraction.

---

## Contributing
Contributions are welcome! Please fork the repository and create a pull request for any features or fixes you would like to contribute.

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
