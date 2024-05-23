import cv2
import xml.etree.ElementTree as ET
from typing import Tuple, Dict

# TODO: Any frame adjustments in here need to be mirrored in my training code!!!
FRAME_OFFSET: int = 2


class VideoAnnotator:
    def __init__(self, video_path: str, annotations_path: str, resize_factor: float = 1.0):
        self.video_path = video_path
        self.annotations_path = annotations_path
        self.resize_factor = resize_factor
        self.gt = self._load_cvat_groundtruth(annotations_path)
        self.prev_frame = None

    def _load_cvat_groundtruth(self, xml_file_path: str) -> dict:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        gt = {"BallPos": []}

        for child in root:
            for subchild in child:
                if "frame" in subchild.attrib:
                    frame = int(subchild.attrib['frame'])
                    x, y = self._extract_coordinates(subchild)
                    gt["BallPos"].append([frame, frame, x, y])

        for image in root.findall('image'):
            image_id = int(image.attrib['id'])
            for points in image.findall('points'):
                if points.attrib['label'] == 'ball':
                    x, y = self._extract_coordinates(points)
                    gt["BallPos"].append([image_id, image_id, x, y])

        return gt

    def _extract_coordinates(self, points) -> Tuple[int, int]:
        x, y = map(float, points.attrib['points'].split(','))
        print(self.resize_factor)
        return int(x * self.resize_factor), int(y * self.resize_factor)

    def annotate_video(self):
        cap = cv2.VideoCapture(self.video_path)
        paused = False

        while cap.isOpened():
            if not paused:
                ret, frame = cap.read()
                if not ret:
                    break

                frame = cv2.resize(frame, (0, 0), fx=self.resize_factor, fy=self.resize_factor)

                if self.prev_frame is not None:
                    for annotation in self.gt['BallPos']:
                        start_frame, end_frame, x, y = annotation
                        if start_frame <= cap.get(cv2.CAP_PROP_POS_FRAMES) - FRAME_OFFSET <= end_frame:
                            cv2.circle(self.prev_frame, (x, y), int(10 * self.resize_factor), (0, 255, 0), -1)

                    cv2.imshow('Frame', self.prev_frame)

                self.prev_frame = frame

            key = cv2.waitKey(30) & 0xFF
            if key == ord('q'):
                break
            elif key == ord(' '):
                paused = not paused

        cap.release()
        cv2.destroyAllWindows()


def main():
    # video_path = r"C:\Users\timf3\PycharmProjects\AFL-Data\marvel\marvel-fov-6\19_05_2024\marvel-fov-6_time_04_21_07_date_19_05_2024_\2.mp4"
    # annotations_path = r"C:\Users\timf3\Downloads\drive-download-20240523T024955Z-001\marvel-fov-6_time_04_21_07_date_19_05_2024_2\marvel-fov-6_time_04_21_07_date_19_05_2024_2.xml"

    video_path = r"C:\Users\timf3\PycharmProjects\AFL-Data\marvel\marvel-fov-2\18_08_2023\marvel2_time_10_24_03_date_19_08_2023_\0.mp4"
    annotations_path = r"C:\Users\timf3\PycharmProjects\AFL-Data\marvel\afl-preprocessed\train\annotations\marvel2_time_10_24_03_date_19_08_2023_0.xml"

    annotator = VideoAnnotator(video_path, annotations_path, resize_factor=0.8)
    annotator.annotate_video()


if __name__ == "__main__":
    main()
