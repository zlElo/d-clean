import os
import shutil

def overwriter(selected_drive):
    print('[log] Write maximum of drive...')
    total, used, free = shutil.disk_usage(selected_drive)
    print(f'[log] Drive size: {total} bytes')
    
    # size of file in bytes
    file_size = total

    # path to file
    file_path = f"{selected_drive}/file.bin"

    # open file in writing mode
    with open(file_path, "wb") as f:
        while os.path.getsize(file_path) < file_size:
            f.write(os.urandom(1024))
