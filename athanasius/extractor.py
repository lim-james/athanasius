import os
import struct
import math

def extract(archive_filename):
    with open(archive_filename, "rb") as archive_file:
        num_files = struct.unpack(">I", archive_file.read(4))[0]
        file_metadata = []

        for _ in range(num_files):
            name_len = struct.unpack(">I", archive_file.read(4))[0]
            name = archive_file.read(name_len).decode("utf-8")
            size = struct.unpack(">Q", archive_file.read(8))[0]
            mode = struct.unpack(">Q", archive_file.read(8))[0]
            mtime = struct.unpack(">d", archive_file.read(8))[0]
            file_metadata.append((name, size, mode, mtime))

        for (name, size, mode, mtime) in file_metadata:
            dir_name = os.path.dirname(name)
            if dir_name:
                os.makedirs(dir_name, exist_ok=True)

            with open(name, "wb") as f:
                f.write(archive_file.read(size))

            try:
                os.chmod(name, mode & 0o7777)

                os.utime(name, (mtime, mtime))
            except OSError as e:
                print(f"Warning: could not restore metadata for {name}: {e}")
