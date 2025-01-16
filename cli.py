import argparse
import os
import json

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

def archive_folder(folder_path, archive_name):
    if not os.path.exists(folder_path):
        print(f"Error: The folder '{folder_path}' does not exist.")
        return

    if not os.path.isdir(folder_path):
        print(f"Error: '{folder_path}' is not a folder.")
        return

    archive_content = {}

    def traverse_folder(path, archive_dict):
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isfile(item_path):
                with open(item_path, 'r') as file:
                    archive_dict[item] = file.read()
            elif os.path.isdir(item_path):
                archive_dict[item] = {}
                traverse_folder(item_path, archive_dict[item])

    try:
        traverse_folder(folder_path, archive_content)

        with open(archive_name, 'w') as archive_file:
            json.dump(archive_content, archive_file)
    except Exception as e:
        print(f"Error: Unable to archive folder. {e}")
        
    
def extract_folder(archive_name, output_folder):
    if not os.path.exists(archive_name):
        print(f"Error: The archive '{archive_name}' does not exists.")
        return
    
    try: 
        with open(archive_name, 'r') as archive_file:
            archive_content = json.load(archive_file)

            def recreate_folder(content, path):
                os.makedirs(path, exist_ok=True)
                for name, data in content.items():
                    item_path = os.path.join(path, name)

                    if isinstance(data, dict):
                        recreate_folder(data, item_path)
                    else:
                        with open(item_path, 'w') as file:
                            file.write(data)

        recreate_folder(archive_content, output_folder)
    except Exception as e:
        print(f"Error: Unable to extract folder. {e}")
    

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["read", "list", "archive", "extract"], help="Action to perform.")
    parser.add_argument("path", help="Path to file or folder.")

    args = parser.parse_args()

    if args.action == "read":
        read_file(args.path)
    elif args.action == "list":
        list_folder(args.path)
    elif args.action == "archive":
        archive_folder(args.path, "archive.ath")
    elif args.action == "extract":
        extract_folder(args.path, "folder")

if __name__ == "__main__":
    main()