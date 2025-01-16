import argparse
import os

def read_file(file_path):
    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' does not exists.")
        return

    if os.path.isdir(file_path):
        print(f"Error: '{file_path}' is a directory. Use the 'list' action instead.")
        return

    try:
        with open(file_path, 'r') as file:
            content = file.read()
            print(file_path)
            print(content)
    except Exception as e:
        print(f"Error: Unable to read the file. {e}")

def list_folder(folder_path):
    if not os.path.exists(folder_path):
        print(f"Error: The folder '{folder_path}' does not exist.")
        return

    if not os.path.isdir(folder_path):
        print(f"Error: '{folder_path}' is not a folder. Use the 'read' action instead.")
        return

    try:
        print(f"Contents of folder '{folder_path}':")
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isdir(item_path):
                print(f"📁 {item}/")
            else:
                print(f"📄 {item}")
    except Exception as e:
        print(f"Error: Unable to list folder contents. {e}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["read", "list"], help="Action to perform: 'read' for file, 'list' for folder.")
    parser.add_argument("path", help="Path to file or folder.")

    args = parser.parse_args()

    if args.action == "read":
        read_file(args.path)
    elif args.action == "list":
        list_folder(args.path)

if __name__ == "__main__":
    main()