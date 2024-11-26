import os
from typing import List, Dict, Tuple
from collections import defaultdict
from glob import glob

from utils import find_files_with_ending

ROOT_DIR: str = r"C:\Users\timf3\PycharmProjects\AFL-Data\marvel"


class AFLDataAnalysis:
    def __init__(self, root_dir: str):
        self.afl_preprocessed_data: str = root_dir
        self.ball_count: Dict[str, int] = {}
        self.splits = ['train', 'val', 'test']
        self.split_image_counts = defaultdict(int)

    def count_labelled_frames(self) -> None:
        """
        Counts the number of labelled frames in the annotations folder.
        """
        # Get a list of the xml files in the annotations folder
        list_of_xml_files: List[str] = find_files_with_ending(self.afl_preprocessed_data, ".xml")

        count = 0

        for xml_file in list_of_xml_files:
            file_name_without_extension = os.path.splitext(os.path.basename(xml_file))[0]
            # Open the xml file
            with open(xml_file, "r") as f:
                # Read the file
                xml_file_content = f.read()

                # Count the number of labelled frames via <points> tags
                count += xml_file_content.count("<points")

                self.ball_count[file_name_without_extension] = count

            count = 0

        for key, value in self.ball_count.items():
            print(f"Ball annotation count is {value} for {key}")
        print("Total number of frames is: ", sum(self.ball_count.values()))

    def analyze_dataset_distribution(self) -> None:
        """
        Analyzes the distribution of images and marvel_{n} folders across train/val/test splits.
        """
        print("\nDataset Distribution Analysis:")
        print("-" * 50)

        for split in self.splits:
            split_path = os.path.join(self.afl_preprocessed_data, "afl-preprocessed", split, "unpacked_png")
            if not os.path.exists(split_path):
                print(f"Warning: {split_path} does not exist")
                continue

            # Count total images in the split
            image_count = 0
            marvel_counts = defaultdict(int)

            # Get all marvel folders in this split
            marvel_folders = [f for f in os.listdir(split_path) if os.path.isdir(os.path.join(split_path, f))]

            for folder in marvel_folders:
                folder_path = os.path.join(split_path, folder)
                # Count images in this folder
                images = glob(os.path.join(folder_path, "*.png"))
                image_count += len(images)

                # Extract marvel number
                if "marvel" in folder.lower():
                    marvel_num = None
                    if "marvel-fov-" in folder.lower():
                        marvel_num = folder.lower().split("marvel-fov-")[1].split("_")[0]
                    else:
                        marvel_num = folder.lower().split("marvel_")[1].split("_")[0]
                    marvel_counts[f"marvel_{marvel_num}"] += 1

            # Store the image count for this split
            self.split_image_counts[split] = image_count

            # Print results for this split
            print(f"\n{split.upper()} Split:")
            print(f"Total images: {image_count}")
            print("Marvel distribution:")
            for marvel_id, count in sorted(marvel_counts.items()):
                print(f"  {marvel_id}: {count} folders")

    def calculate_split_ratios(self) -> None:
        """
        Calculates and prints the ratio of images in train:val:test splits as percentages.
        """
        total_images = sum(self.split_image_counts.values())

        if total_images == 0:
            print("\nWarning: No images found in any split")
            return

        print("\nDataset Split Ratios:")
        print("-" * 50)
        for split in self.splits:
            percentage = (self.split_image_counts[split] / total_images) * 100
            print(f"{split}: {percentage:.1f}%")

        print(f"\nSplit ratio (train:val:test) = "
              f"{self.split_image_counts['train']:.1f}:"
              f"{self.split_image_counts['val']:.1f}:"
              f"{self.split_image_counts['test']:.1f}")

    def print_dataset_summary(self) -> None:
        """
        Prints an overall summary of the dataset.
        """
        print("\nOverall Dataset Summary:")
        print("-" * 50)
        total_images = 0
        all_marvel_counts = defaultdict(int)

        for split in self.splits:
            split_path = os.path.join(self.afl_preprocessed_data, "afl-preprocessed", split, "unpacked_png")
            if not os.path.exists(split_path):
                continue

            marvel_folders = [f for f in os.listdir(split_path) if os.path.isdir(os.path.join(split_path, f))]

            for folder in marvel_folders:
                folder_path = os.path.join(split_path, folder)
                images = glob(os.path.join(folder_path, "*.png"))
                total_images += len(images)

                if "marvel" in folder.lower():
                    marvel_num = None
                    if "marvel-fov-" in folder.lower():
                        marvel_num = folder.lower().split("marvel-fov-")[1].split("_")[0]
                    else:
                        marvel_num = folder.lower().split("marvel_")[1].split("_")[0]
                    all_marvel_counts[f"marvel_{marvel_num}"] += 1

        print(f"Total images across all splits: {total_images}")
        print("\nOverall Marvel distribution:")
        for marvel_id, count in sorted(all_marvel_counts.items()):
            print(f"  {marvel_id}: {count} folders total")


def main():
    bohs_data_analysis = AFLDataAnalysis(ROOT_DIR)
    bohs_data_analysis.count_labelled_frames()
    bohs_data_analysis.analyze_dataset_distribution()
    bohs_data_analysis.calculate_split_ratios()
    bohs_data_analysis.print_dataset_summary()


if __name__ == "__main__":
    main()