import os

from typing import List


def ensure_directory_exists(path: str) -> None:
    """
    Ensures that the directory at the specified path exists.

    Args:
    path (str): Path to the directory.

    Returns:
    None
    """
    if not os.path.exists(path):
        os.makedirs(path)


def create_directory(base_path: str, directory_name: str) -> str:
    """
    Creates a directory inside the base_path with the specified name if it doesn't already exist.

    Args:
    base_path (str): Base path where the directory should be created.
    directory_name (str): Name of the directory to be created.

    Returns:
    str: Path to the created directory.
    """
    dir_path = os.path.join(base_path, directory_name)
    ensure_directory_exists(dir_path)
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

def files_exist_with_extension(directory: str, extension: str) -> bool:
    """
    Check if files with the specified extension exist in the given directory.

    Args:
    directory (str): Path to the directory to search in.
    extension (str): File extension to search for.

    Returns:
    bool: True if any files with the given extension are found, otherwise False.
    """
    return any(f.endswith(extension) for f in os.listdir(directory))

def mp4_files_exist(directory: str) -> bool:
    """Check if .mp4 files exist in the given directory."""
    return files_exist_with_extension(directory, '.mp4')


def png_files_exist(directory: str) -> bool:
    """Check if .png files exist in the given directory."""
    return files_exist_with_extension(directory, '.png')
