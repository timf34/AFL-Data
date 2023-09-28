"""
Temporary script to shift our images frame number down by one. (i.e. img00001.png -> img00000.png)

DO NOT RUN THIS SCRIPT MORE THAN ONCE! IT'S NOW BEEN FIXED!
"""

import os
from typing import List
from utils import find_files_with_ending

ROOT_DIR: str = r"C:\Users\timf3\PycharmProjects\AFL-Data\marvel"


def shift_image_names(directory: str):
    # Get all the PNG files
    all_png_files = find_files_with_ending(directory, '.png')

    # Sort them in reverse so that we're renaming the last file first.
    # This way, we don't overwrite any file.
    all_png_files.sort()

    for file_path in all_png_files:
        dir_name, file_name = os.path.split(file_path)
        # Check if the file matches the pattern imgXXXXX.png
        if file_name.startswith("img") and len(file_name) == 12:
            # Extract the number part
            num = int(file_name[3:8])

            # Decrement the number by one
            new_num = num - 1

            # Format the new number and create the new name
            new_name = f"img{new_num:05}.png"
            new_path = os.path.join(dir_name, new_name)

            # Rename the file
            os.rename(file_path, new_path)
            # print(f"Would rename {file_p ath} -> {new_path}")
            print(f"Renamed {file_path} -> {new_path}")


if __name__ == "__main__":
    # shift_image_names(ROOT_DIR)
    print("Careful there cowboy")