import boto3
from typing import List

BUCKET_NAME: str = 'australia-fov'
PATH_PREFIX: str = 'marvel/'
REGION: str = 'ap-southeast-2'
CAMERAS: List[str] = [
    "marvel-fov-1/",
    "marvel-fov-2/",
    "marvel-fov-3/",
    "marvel-fov-4/",
    "marvel-fov-5/",
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
    s3 = boto3.client('s3', region_name=REGION)

    for camera in CAMERAS:
        for postfix in PATH_POSTFIXES:
            # Constructing the path to the desired video
            camera_path = PATH_PREFIX + camera + postfix
            response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=camera_path)

            # Filtering out only the video files and sorting them
            video_files = sorted(
                [content['Key'] for content in response.get('Contents', []) if content['Key'].endswith('.avi')])

            # Print the first video from the list if available
            if video_files:
                print(video_files[0])


if __name__ == "__main__":
    main()
