"""
This script takes a video and a cvat annotation file and visualises the annotations on the video.
"""
import cv2
import os
import xml.etree.ElementTree as ET

from typing import Tuple, Dict

VIDEO_PATH: str = r"C:\Users\timf3\PycharmProjects\AFL-Data\marvel\marvel-fov-8\18_08_2023\marvel8_time_10_24_04_date_19_08_2023_\1.mp4"
CVAT_ANNOTATIONS: str = r"C:\Users\timf3\PycharmProjects\AFL-Data\marvel\afl-preprocessed\train\annotations\marvel8_time_10_24_04_date_19_08_2023_1.xml"


def _load_cvat_groundtruth(xml_file_path: str) -> dict:
    """
    This function reads and loads the xml file into a dictionary which we will
    then pass to _create_bohs_annotations...

    In general, this will read the groundtruth xml file, to extract frame and x-y position

    :params xml_file_path: path to the xml file
    :returns: dictionary of ball positions
    The structure of this dictionary is as follows:
        {'BallPos': [[382, 382, 437, 782]
        ... where the elements of the list are as follows [start_frame, end_frame, x, y]
    """

    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    gt = {"BallPos": []}

    # Handle XML structure with "frame" attributes (from videos uploaded to CVAT)
    for child in root:
        for subchild in child:
            if "frame" in subchild.attrib:
                # print("frame:", subchild.attrib['frame'], "x:", subchild.attrib['points'].split(',')[0], "y:",  \
                # subchild.attrib['points'].split(',')[1])

                frame = int(subchild.attrib['frame'])
                x, y = _extract_coordinates(subchild)

                # We put frame in twice simply to match FootAndBall dataloader
                gt["BallPos"].append([frame, frame, x, y])

    # Handle XML structure with "frame" attributes (from folders of images uploaded to CVAT)
    for image in root.findall('image'):
        image_id = int(image.attrib['id'])

        for points in image.findall('points'):
            if points.attrib['label'] == 'ball':
                # Extracting x, y coordinates from points
                x, y = _extract_coordinates(points)
                # Append to the dictionary
                gt["BallPos"].append([image_id, image_id, x, y])
    return gt


def _extract_coordinates(points) -> Tuple[int, int]:
    x, y = map(float, points.attrib['points'].split(','))
    return int(x), int(y)


def main():
    # Load the video
    cap = cv2.VideoCapture(VIDEO_PATH)

    # Load the annotations
    gt = _load_cvat_groundtruth(CVAT_ANNOTATIONS)

    # Iterate through the video
    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        # Draw the annotations on the frame
        for annotation in gt['BallPos']:
            start_frame, end_frame, x, y = annotation
            if start_frame <= cap.get(cv2.CAP_PROP_POS_FRAMES) <= end_frame:
                cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)


        # Display the frame
        cv2.imshow('Frame', frame)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the VideoCapture and VideoWriter objects
    cap.release()

    # Destroy all windows
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()