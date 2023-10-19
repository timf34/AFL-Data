"""
This is a temporary script.

For xml files from datasets that were uploaded as a group of frames rather than videos, there's a mismatch between
the `id` and the `name`. The `id` might be `4` which is the correct number for the frame (i.e. frame_0000004.png)
but the name attribute is actually just completely wrong (its img00005.jpg instead of frame_0000004.png).

So I think I'll just get rid of the name attribute all together. It's confusing things.
"""
import os
from typing import List
from utils import find_files_with_ending
import xml.etree.ElementTree as ET


ROOT_DIR: str = r"C:\Users\timf3\PycharmProjects\AFL-Data\marvel"

def remove_name_attr(xml_file_path: str) -> None:

    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    for image in root.findall('image'):
        # Removing the "name" attribute
        if 'name' in image.attrib:
            image.attrib.pop('name')

    # Save the modified XML back to the file
    tree.write(xml_file_path)


def remove_name_attr_from_xml_files(dir: str) -> None:
    all_xml_files = find_files_with_ending(dir, '.xml')

    for file_path in all_xml_files:
        # Make sure the file exists, if not, print an error
        if os.path.exists(file_path):
            remove_name_attr(file_path)
            print(f"Removed name attr from {file_path}")
        else:
            print(f"File {file_path} not found!")


def main():
    remove_name_attr_from_xml_files(ROOT_DIR)


if __name__ == '__main__':
    main()
