import os

from typing import List

def mp4_files_exist(directory: str) -> bool:
    """Check if .mp4 files exist in the given directory."""
    return any([f for f in os.listdir(directory) if f.endswith('.mp4')])


def check_dir(path: str) -> None:
    if not os.path.exists(path):
        print(f"Creating directory: {path}")
        os.makedirs(path)

def create_directory(base_path: str, directory_name: str) -> str:
    """Creates a directory if it doesn't already exist."""
    dir_path = os.path.join(base_path, directory_name)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return dir_path

def find_files_with_ending(directory: str, file_ending: str = '.avi') -> List[str]:
    """
    Find all files and subfile paths in a directory with the given file ending.

    Args:
    directory (str): Path to the directory to search in.
    file_ending (str): Desired file ending, e.g., '.avi', '.mp4', etc.

    Returns:
    List[str]: List of paths to files with the given ending.
    """
    matched_files = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(file_ending):
                matched_files.append(os.path.join(root, file))

    return matched_files

def png_files_exist(directory: str) -> bool:
    """
    Check if any .png files exist in the given directory.

    Args:
    directory (str): Path to the directory to search in.

    Returns:
    bool: True if any .png files are found, otherwise False.
    """
    for file in os.listdir(directory):
        if file.endswith('.png'):
            return True
    return False
