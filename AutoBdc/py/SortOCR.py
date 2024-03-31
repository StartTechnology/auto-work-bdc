import os
import shutil
import time

#file_path = ""
#folder_path = "./_delete_"

def move_file_to_folder(file_path, folder_path):
    try:
        shutil.move(file_path, folder_path)
        print(f"Moved {file_path} to {folder_path}")
    except Exception as e:
        print(f"Error moving file: {e}")


print(time.strftime("%Y%m%d", time.localtime()))