"""
We are splitting our train/ val/ test set very simply by putting each into a given folder.

This script writes which files are in which folder (i.e. train/ val/ test) to a text file.

It also ensures that there are no duplicates.

TODO: Make it check that each image path exists!
"""

import os
from typing import Dict, List
from utils import find_files_with_ending


FILE_RECORD_NAME: str = "dataset_partitioning_record.txt"

def list_files_in_folders(root_folder: str, sub_folders: List[str], file_ending: str) -> Dict[str, List[str]]:
    """Returns a dictionary with folder names as keys and list of files in each folder as values"""
    all_files = {}
    for folder in sub_folders:
        folder_path = os.path.join(root_folder, folder)
        all_files[folder] = find_files_with_ending(folder_path, file_ending)
    return all_files

def check_for_duplicates(all_files: Dict) -> None:
    """Raises an error if there are duplicate files across folders"""
    all_file_names = []
    for folder, files in all_files.items():
        all_file_names.extend(files)

    unique_files = set(all_file_names)
    if len(unique_files) != len(all_file_names):
        raise ValueError("There are duplicate files across folders!")


def check_corresponding_folders_exist(all_files: Dict[str, List[str]], root_folder: str) -> None:
    for folder, files in all_files.items():
        for file in files:
            # Extract the filename without the extension to get the corresponding folder name
            folder_name = os.path.splitext(os.path.basename(file))[0]
            corresponding_folder = os.path.join(root_folder, folder, "unpacked_png", folder_name)

            if not os.path.isdir(corresponding_folder):
                raise ValueError(f"The folder {corresponding_folder} does not exist for the XML file {file}.")

def write_files_to_text(all_files:  Dict[str, List[str]], output_file: str) -> None:
    """Writes the list of files from all folders to a text file"""
    with open(output_file, 'w') as f:
        for folder, files in all_files.items():
            f.write(f"Files in {folder}:\n")
            for file_name in files:
                f.write(file_name + "\n")
            f.write("\n")

if __name__ == "__main__":
    root_folder = 'marvel/afl-preprocessed'  # Assuming datasets folder has train, val, test subfolders
    sub_folders = ['train', 'val', 'test']
    file_ending = ".xml"

    all_files = list_files_in_folders(root_folder, sub_folders, file_ending)
    check_for_duplicates(all_files)
    check_corresponding_folders_exist(all_files, root_folder)
    write_files_to_text(all_files, FILE_RECORD_NAME)
