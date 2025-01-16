import argparse
import os

def read_file(file_path):
    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' does not exists.")
        return

    try:
        with open(file_path, 'r') as file:
            content = file.read()
            print(file_path)
            print(content)
    except Exception as e:
        print(f"Error: Unable to read the file. {e}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="Path to file to be read.")

    args = parser.parse_args()

    read_file(args.file)

if __name__ == "__main__":
    main()