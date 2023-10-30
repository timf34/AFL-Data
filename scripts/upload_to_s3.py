import boto3
import os
from botocore.exceptions import NoCredentialsError


AUS_AFL_BUCKET: str = "australia-fov"
DUB_AFL_BUCKET: str = "dublin-afl-preprocessed"
ANNOTATIONS_FOLDER: str = "annotations"

S3_PREFIX: str = "train/unpacked_png/"  # Ensure it ends with "/"

# Ensure that each video path exists on s3
s3 = boto3.client('s3')


def upload_folder_to_s3(folder_path: str, bucket: str, prefix: str) -> None:
    """
    Uploads all .png files from a given folder to a specified S3 bucket and prefix.

    Parameters:
    - folder_path (str): Local path to the folder containing .png files
    - bucket (str): Name of the S3 bucket to upload to
    - prefix (str): S3 prefix (folder) to upload the files to

    Returns:
    - None
    """
    if not os.path.exists(folder_path):
        print(f"Folder {folder_path} does not exist!")
        return
    else:
        print(f"Uploading {folder_path} to {bucket}{prefix}")

    folder_name = os.path.basename(folder_path)

    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            if filename.endswith('.txt'):
                local_path = os.path.join(root, filename)
                s3_path = prefix + folder_name + "/" + filename

                try:
                    s3.upload_file(local_path, bucket, s3_path)
                    print(f"Uploaded {filename} to {bucket}/{s3_path}")
                except NoCredentialsError:
                    print("Credentials not available")


def main():
    upload_folder_to_s3(r"C:\Users\timf3\PycharmProjects\AFL-Data\scripts\yolo", DUB_AFL_BUCKET, S3_PREFIX)


if __name__ == '__main__':
    main()
