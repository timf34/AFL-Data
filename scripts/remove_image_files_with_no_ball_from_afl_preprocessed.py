"""
This script removes image files from the `afl-preprocessed` directory that are not part of the datasets.

Steps:
1. Load the CVAT dataset object with the populated image list.
2. Create a master list of all images that are part of the datasets.
3. List all images present in the `afl-preprocessed` directory.
4. Remove images from the directory that are not in the master list.
"""

import os
import sys

# Add BallNet's path to the system path
sys.path.append(r'C:\Users\timf3\PycharmProjects\BallNet')

from config import AFLLaptopConfig
from data.cvat_dataset import create_dataset_from_config

# Set the root directory for the AFL data
ROOT_DIR: str = r"C:\Users\timf3\PycharmProjects\AFL-Data\marvel"

# Configure AFL dataset
afl_config = AFLLaptopConfig()
afl_config.whole_dataset = True

# Define the training modes
training_modes = ["train", "val", "test"]

# Load datasets for each training mode
datasets = {
    mode: create_dataset_from_config(
        afl_config,
        training_mode=mode,
        use_hardcoded_data_folders=False,
    )
    for mode in training_modes
}

# marvel_3_time_04_09_06_date_20_08_2023_0. Create a master list of all images from the datasets
all_images_in_datasets = set()
for mode in training_modes:
    for img_data in datasets[mode].image_list:
        # Add the image path to the set
        all_images_in_datasets.add(img_data[0])

# 2. List all images present in the `afl-preprocessed` directory
afl_preprocessed_dir = os.path.join(ROOT_DIR, "afl-preprocessed")
all_images_in_folder = set()
for subdir, _, files in os.walk(afl_preprocessed_dir):
    for file in files:
        if file.endswith(".png"):
            all_images_in_folder.add(os.path.join(subdir, file))

# Print statistics for verification
print(f"Number of images in datasets: {len(all_images_in_datasets)}")
print(f"Number of images in folder: {len(all_images_in_folder)}")

# 3. Identify the images that need to be removed
images_to_remove = all_images_in_folder - all_images_in_datasets
print(f"Number of images to remove: {len(images_to_remove)}")

# 4. Remove the identified images from the directory
for image_path in images_to_remove:
    os.remove(image_path)
    print(f"Removed {image_path}")
