import os
import xml.etree.ElementTree as ET

from typing import List, Dict


def process_cvat_annotations(annotations_file: str) -> Dict[int, List[int]]:

    # Check if annotations file exists and is a .xml file
    if not os.path.exists(annotations_file):
        raise FileNotFoundError("Annotations file does not exist.")
    if not annotations_file.endswith(".xml"):
        raise ValueError("Annotations file must be a .xml file.")

    annotations: Dict[int, List[int, int]] = {}

    tree = ET.parse(annotations_file)
    root = tree.getroot()
    for child in root:
        for subchild in child:
            if "frame" in subchild.attrib:
                frame = int(subchild.attrib['frame'])
                x = int(float(subchild.attrib['points'].split(',')[0]))
                y = int(float(subchild.attrib['points'].split(',')[1]))
                annotations[frame] = [x, y]

    # Sort the dictionary by key and return
    return {k: annotations[k] for k in sorted(annotations)}


def ensure_directory_exists(path: str) -> None:
    """
    Ensures that the directory at the specified path exists.

    Args:
    path (str): Path to the directory.

    Returns:
    None
    """

    if not os.path.exists(path):
        print(f'Creating directory at {path}')
        os.makedirs(path)
    else:
        print(f'Directory already exists at {path}')


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

    print(f"Found {len(matched_files)} files with ending {file_ending} in {directory}")

    return matched_files


def count_files_with_extension(directory: str, extension: str) -> int:
    """
    Count the files with the specified extension in the given directory.

    Args:
    directory (str): Path to the directory to search in.
    extension (str): File extension to search for.

    Returns:
    int: Number of files with the given extension found.
    """
    return sum(f.endswith(extension) for f in os.listdir(directory))


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


def get_file_size_in_bytes(file_path: str) -> int:
    """
    Get the size of a file in bytes.

    Parameters:
    - file_path: Path to the file.

    Returns:
    - Size of the file in bytes.
    """
    return os.path.getsize(file_path)


def get_frames_containing_ball(xml_file_path: str) -> List[int]:
    """
    Parse an XML file containing ground truth annotations to identify frames which contain the ball.

    This function specifically handles two XML structures:
    1. XML structure with "frame" attributes typically found from videos uploaded to CVAT.
    2. XML structure with "frame" attributes found from folders of images uploaded to CVAT.

    Args:
        xml_file_path (str): Path to the XML file containing ground truth annotations.

    Returns:
        List[int]: A list of unique frame numbers or image IDs containing the ball.
    """
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    frames_containing_ball = []

    # Handle XML structure with "frame" attributes (from videos uploaded to CVAT)
    for child in root:
        for subchild in child:
            if "frame" in subchild.attrib:
                frame = int(subchild.attrib['frame'])
                if frame not in frames_containing_ball:
                    frames_containing_ball.append(frame)

    # Handle XML structure with "frame" attributes (from folders of images uploaded to CVAT)
    for image in root.findall('image'):
        image_id = int(image.attrib['id'])

        for points in image.findall('points'):
            if points.attrib['label'] == 'ball' and image_id not in frames_containing_ball:
                frames_containing_ball.append(image_id)

    return frames_containing_ball


def get_frame_name_from_frame_number(frame_number: int) -> str:
    """Returns the name of the frame from the frame number"""
    return f"frame_{frame_number:07d}.png"
