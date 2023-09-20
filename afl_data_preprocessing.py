"""
This script will primarily split the .avi videos into individual frames
"""
import os
import subprocess

from typing import List

AFL_DATA_DIR: str = r'/marvel'

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

def create_directory(base_path: str, directory_name: str) -> str:
    """Creates a directory if it doesn't already exist."""
    dir_path = os.path.join(base_path, directory_name)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return dir_path

def extract_frames_from_video(file_path: str) -> None:
    """Given a .avi video file path, extract frames using ffmpeg."""

    # Create a directory called "frames"
    file_dir = os.path.dirname(file_path)
    frames_dir = create_directory(file_dir, directory_name='frames')

    if png_files_exist(frames_dir):
        print(f'Frames already exist in {frames_dir}')
        return

    # Construct the ffmpeg command
    cmd = [
        'ffmpeg',
        '-i', file_path,
        '-vf', 'fps=30/1',
        f'{frames_dir}\\img%05d.png'
    ]

    # Execute the command via subprocess
    print(cmd)
    subprocess.run(cmd)


def main():
    avi_files = find_files_with_ending(r"C:\Users\timf3\PycharmProjects\AFL-Data\marvel", file_ending='.avi')
    for avi_file in avi_files:
        extract_frames_from_video(avi_file)


if __name__ == '__main__':
    main()
