"""
Adding this script although I never wrote down how to use it... I think it compares our local folder to S3 for
differences
"""

import boto3
import os

from typing import List, Dict

s3 = boto3.client('s3')


def count_files_in_s3_folder(bucket_name, folder_path) -> int:
    paginator = s3.get_paginator('list_objects_v2')

    count = 0
    for page in paginator.paginate(Bucket=bucket_name, Prefix=folder_path):
        for obj in page.get('Contents', []):
            count += 1

    return count


def list_leaf_folders(bucket_name):
    s3 = boto3.client('s3')
    paginator = s3.get_paginator('list_objects_v2')

    # This set holds all paths ending with '/' indicating they're directories/folders
    all_folders = set()

    # This set holds paths of directories that have sub-directories
    non_leaf_folders = set()

    # Populate the all_folders set
    for page in paginator.paginate(Bucket=bucket_name):
        for obj in page.get('Contents', []):
            key = obj['Key']
            parts = key.split('/')
            for i in range(1, len(parts)):
                folder = '/'.join(parts[:i]) + '/'
                all_folders.add(folder)
                if i != len(parts) - 1:  # not the last part
                    non_leaf_folders.add(folder)

    # Leaf folders are those in all_folders but not in non_leaf_folders
    leaf_folders = all_folders - non_leaf_folders

    return list(leaf_folders)


bucket = "dublin-afl-preprocessed"
folder = "train/unpacked_png/marvel_1_time_04_09_04_date_20_08_2023_0/"

file_count = count_files_in_s3_folder(bucket, folder)

print(file_count)

leaf_folders = list_leaf_folders(bucket)
for folder in leaf_folders:
    print(folder)