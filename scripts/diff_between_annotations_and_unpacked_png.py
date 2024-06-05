"""
Lists the directories that are missing in the unpacked_png directory corresponding to the XML files in the annotations
directory.
"""
import os

ANNOTATIONS_DIR: str = "../marvel/afl-preprocessed/train/annotations"
UNPACKED_PNG_DIR: str = "../marvel/afl-preprocessed/train/unpacked_png"

xml_files = [xml_file for xml_file in os.listdir(ANNOTATIONS_DIR) if xml_file.endswith('.xml')]
xml_files_stripped = {file[:-4] for file in xml_files}

directories = [dir for dir in os.listdir(UNPACKED_PNG_DIR) if os.path.isdir(os.path.join(UNPACKED_PNG_DIR, dir))]

# Convert directories list to a set for comparison
directories_set = set(directories)

# Find the missing directories
missing_directories = sorted(xml_files_stripped - directories_set)

print("Missing directories corresponding to XML files:")
for dir in missing_directories:
    print(dir)
