# Temp script just to be able to list the video objects for each camera for each day

import boto3
import os
from typing import List
from tqdm import tqdm
import botocore

BUCKET_NAME: str = 'australia-fov'
PATH_PREFIX: str = 'marvel/'
REGION: str = 'ap-southeast-2'
CAMERAS: List[str] = [
    "marvel-fov-1/",
    "marvel-fov-2/",
    "marvel-fov-3/",
    "marvel-fov-4/",
    "marvel-fov-5",
    "marvel-fov-6/",
    "marvel-fov-7/",
    "marvel-fov-8/",
]

PATH_POSTFIXES: List[str] = [
    "18_08_2023/",
    "20_08_2023/",
    "26_08_2023/"
]

def main():

    s3 = boto3.client('s3', region_name="ap-southeast-2")

    for camera in CAMERAS:
        for postfix in PATH_POSTFIXES:
            # Constructing the path to the desired video
            camera_path = PATH_PREFIX + camera + postfix
            # print(camera_path)
            response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=camera_path)
            print(response)


if __name__ == "__main__":
    main()
