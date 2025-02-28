import os
import struct

def archive(paths, output_filename):
    file_entries = []

    for path in paths:
        path = os.path.normpath(path)
        if not os.path.exists(path):
            print(f"Warning: {path} does not exist, skipping.")
            continue

        if os.path.isdir(path):
            for root, _, files in os.walk(path):
                for file in files:
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, start=os.path.dirname(path))
                    file_entries.append((rel_path, full_path))
        else:
            rel_path = os.path.basename(path)
            file_entries.append((rel_path, path))

    with open(output_filename, "wb") as archive_file:
        archive_file.write(struct.pack(">I", len(file_entries)))

        for rel_path, full_path in file_entries:
            stat_info = os.stat(full_path)
            name_bytes = rel_path.encode("utf-8")
            size = stat_info.st_size
            mode = stat_info.st_mode
            mtime = stat_info.st_mtime

            archive_file.write(struct.pack(">I", len(name_bytes)))
            archive_file.write(name_bytes)
            archive_file.write(struct.pack(">Q", size))
            archive_file.write(struct.pack(">Q", mode))
            archive_file.write(struct.pack(">d", mtime))

        for _, full_path in file_entries:
            with open(full_path, "rb") as f:
                archive_file.write(f.read())
