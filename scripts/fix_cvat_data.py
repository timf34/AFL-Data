"""
Temporary script to shift our images frame number down by one. (i.e. img00001.png -> img00000.png)

Also a temporary script to rename our images from imgXXXXX.png to frame_XXXXXXX.jpg to match Bohs naming convention.

DO NOT RUN THIS SCRIPT MORE THAN ONCE! IT'S NOW BEEN FIXED!
"""

import os
from typing import List
from utils import find_files_with_ending

ROOT_DIR: str = r"C:\Users\timf3\PycharmProjects\AFL-Data\test-marvel"


def shift_image_names(directory: str):
    confirm = input("Are you sure you want to run `shift_image_names`? (yes/no): ").strip().lower()

    if confirm != "yes":
        print("Script execution aborted.")
        return

    print("Again... are you sure you want to run `shift_image_names`?")
    confirm = input("Type 'yes' to confirm: ").strip().lower()

    if confirm != "yes":
        print("Script execution aborted.")
        return


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


def rename_images(directory: str, file_extension: str = '.png') -> None:
    """Function to rename our images from imgXXXXX.png to frame_XXXXXXX.png to match Bohs naming convention."""

    # Verification Step
    confirm_dir = input(f"You've entered the directory as: {directory}. Is this correct? (yes/no): ").strip().lower()
    if confirm_dir != 'yes':
        print("Operation cancelled.")
        return

    confirm_ext = input(f"You've entered the file extension as: {file_extension}. Is this correct? (yes/no): ").strip().lower()
    if confirm_ext != 'yes':
        print("Operation cancelled.")
        return

    all_png_files = find_files_with_ending(directory, file_extension)

    for png_file in all_png_files:
        basename = os.path.basename(png_file)
        filename, _ = os.path.splitext(basename)

        # Assuming original filenames are in the format imgXXXXX.png
        if filename.startswith('img'):
            frame_number = filename[3:]  # Strip 'img' prefix
            frame_number = frame_number.zfill(7)  # Pad with zeros to reach 7 digits

            # Create new filename and its full path
            new_filename = f'frame_{frame_number}{file_extension}'
            new_path = os.path.join(os.path.dirname(png_file), new_filename)

            # Rename the file
            os.rename(png_file, new_path)


if __name__ == "__main__":
    # shift_image_names(ROOT_DIR)
    rename_images(ROOT_DIR)
    print("Careful there cowboy")