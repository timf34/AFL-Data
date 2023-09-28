import os
from typing import List, Dict

from utils import process_cvat_annotations, find_files_with_ending


class AFLDataAnalysis:
    def __init__(self):
        self.bohs_preprocessed_root_dir: str = r"C:\Users\timf3\PycharmProjects\AFL-Data\marvel\marvel-fov-1\20_08_2023\marvel_1_time_04_09_04_date_20_08_2023_"
        self.ball_count: Dict[str, int] = {}

    def count_lablled_frames(self) -> None:
        """
            Counts the number of labelled frames in the annotations folder.
        """
        # Get a list of the xml files in the annotations folder
        list_of_xml_files: List[str] = find_files_with_ending(self.bohs_preprocessed_root_dir, ".xml")

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

            # print(f"Ball annotation count is {count} for {xml_file}")
            count = 0

        for key, value in self.ball_count.items():
            print(f"Ball annotation count is {value} for {key}")
        print("Total number of frames is: ", sum(self.ball_count.values()))


def main():
    bohs_data_analysis = AFLDataAnalysis()
    bohs_data_analysis.count_lablled_frames()


if __name__ == "__main__":
    main()
