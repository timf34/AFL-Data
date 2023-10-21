"""
Script to remove image files that don't contain the ball from `afl-preprocessed`

Plan:

1. Just load the CVAT dataset object with the populated image list
"""


import os
import sys
import xml.etree.ElementTree as ET

from typing import List, Dict

sys.path.append(r'C:\Users\timf3\PycharmProjects\BallNet')
ROOT_DIR: str = r"C:\Users\timf3\PycharmProjects\AFL-Data\marvel"

from config import AFLLaptopConfig
from data.cvat_dataset import create_dataset_from_config

afl_config = AFLLaptopConfig()
afl_config.whole_dataset = True

training_modes = ["train", "val", "test"]

datasets = {
    mode: create_dataset_from_config(
        afl_config,
        training_mode=mode,
        use_hardcoded_data_folders=False,
    )
    for mode in training_modes
}

# 1. Create a master list of all images from the datasets
all_images_in_datasets = set()
for mode in training_modes:
    for img_data in datasets[mode].image_list:
        all_images_in_datasets.add(img_data[0]) # Assuming the first item in the tuple is the image path


# 2. List all images present in the `afl-preprocessed` folder
afl_preprocessed_dir = os.path.join(ROOT_DIR, "afl-preprocessed")
all_images_in_folder = set()

for subdir, _, files in os.walk(afl_preprocessed_dir):
    for file in files:
        if file.endswith(".png"):
            all_images_in_folder.add(os.path.join(subdir, file))

# Print the number of images in each set
print(f"Number of images in datasets: {len(all_images_in_datasets)}")
print(f"Number of images in folder: {len(all_images_in_folder)}")

# 3. Find the difference between the two sets
images_to_remove = all_images_in_folder - all_images_in_datasets

print(f"Number of images to remove: {len(images_to_remove)}")

# 4. Remove the images from the folder
for image_path in images_to_remove:
    os.remove(image_path)
    print(f"Removed {image_path}")
