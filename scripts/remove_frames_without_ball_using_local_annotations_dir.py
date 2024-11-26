"""
Script for removing frames without a ball in them from the AFL dataset **locally**.

Note: this works by using the local `annotations` directory

"""

import cv2
from sagemaker_utils import *
import os
from typing import List, Dict

# Folder path
FOLDERS: List[str] = [
    "../marvel/afl-preprocessed/train/unpacked_png",
    "../marvel/afl-preprocessed/test/unpacked_png",
    "../marvel/afl-preprocessed/val/unpacked_png",
]
ANNOTATIONS_FOLDER: str = "../annotations"

# Initialize global count variable
# TODO: what does this measure? I think its just all .png files...?
count = 0


def list_directories(path='.') -> List[str]:
    """
    List all directories at the given path.

    :param path: The path where to look for directories.
    :return: A list of directory names.
    """
    return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]


def remove_frames_without_ball(video_name: str, image_folder_path: str, annotations_folder: str) -> None:
    global count  # Declare the count as global to modify it

    xml_file_path = os.path.join(annotations_folder, f"{video_name}.xml")

    # Ensure the xml file exists
    if not os.path.exists(xml_file_path):
        print(f"File {xml_file_path} does not exist. Returning...")
        return

    frame_nums: List[int] = get_frames_containing_ball(xml_file_path)
    file_names: List[str] = [get_frame_name_from_frame_number(frame_num) for frame_num in frame_nums]

    extracted_image_files: List[str] = find_files_with_ending(f"{image_folder_path}/{video_name}", ".png")

    count += len(extracted_image_files)

    for file in extracted_image_files:
        file_name = os.path.basename(file)
        if file_name not in file_names:
            # os.remove(file)
            print(f"Removing {file}")


def main():
    for path in FOLDERS:
        image_folders = list_directories(path)
        for image_folder_name in image_folders:
            remove_frames_without_ball(image_folder_name, path, ANNOTATIONS_FOLDER)

    print(count)


if __name__ == '__main__':
    main()
