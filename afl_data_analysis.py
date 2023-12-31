import os
from typing import List, Dict

from utils import find_files_with_ending

ROOT_DIR: str = r"C:\Users\timf3\PycharmProjects\AFL-Data\marvel"


class AFLDataAnalysis:
    def __init__(self, root_dir: str):
        self.afl_preprocessed_data: str = root_dir
        self.ball_count: Dict[str, int] = {}

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

            # print(f"Ball annotation count is {count} for {xml_file}")
            count = 0

        for key, value in self.ball_count.items():
            print(f"Ball annotation count is {value} for {key}")
        print("Total number of frames is: ", sum(self.ball_count.values()))


def main():
    bohs_data_analysis = AFLDataAnalysis(ROOT_DIR)
    bohs_data_analysis.count_labelled_frames()


if __name__ == "__main__":
    main()
