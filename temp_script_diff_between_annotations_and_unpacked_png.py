"""
Scripts for getting these, ran from python console in terminal in the same directory as annotaions and unpacked_png

import os

def list_directories():
    cwd = os.getcwd()
    return [d for d in os.listdir(cwd) if os.path.isdir(os.path.join(cwd, d))]

print(list_directories())


import os

def list_xml_files():
    cwd = os.getcwd()
    return [f for f in os.listdir(cwd) if f.endswith('.xml')]

print(list_xml_files())
"""

xml_files = ['marvel1_time_10_24_03_date_19_08_2023_0.xml', 'marvel1_time_10_24_03_date_19_08_2023_1.xml', 'marvel2_time_10_24_03_date_19_08_2023_0.xml', 'marvel2_time_10_24_03_date_19_08_2023_1.xml', 'marvel3_time_09_09_04_date_27_08_2023_0.xml', 'marvel3_time_10_24_03_date_19_08_2023_0.xml', 'marvel3_time_10_24_03_date_19_08_2023_1.xml', 'marvel7_time_10_24_03_date_19_08_2023_0.xml', 'marvel7_time_10_24_03_date_19_08_2023_1.xml', 'marvel8_time_10_24_04_date_19_08_2023_0.xml', 'marvel8_time_10_24_04_date_19_08_2023_1.xml', 'marvel_1_time_04_09_04_date_20_08_2023_0.xml', 'marvel_1_time_04_09_04_date_20_08_2023_3.xml', 'marvel_1_time_04_09_04_date_20_08_2023_4.xml', 'marvel_1_time_04_09_04_date_20_08_2023_5.xml', 'marvel_1_time_04_09_04_date_20_08_2023_6.xml', 'marvel_1_time_04_09_04_date_20_08_2023_7.xml', 'marvel_3_time_04_09_06_date_20_08_2023_0.xml', 'marvel_3_time_04_09_06_date_20_08_2023_1.xml', 'marvel_3_time_04_09_06_date_20_08_2023_2.xml', 'marvel_3_time_04_09_06_date_20_08_2023_3.xml', 'marvel_3_time_04_09_06_date_20_08_2023_5.xml', 'marvel_3_time_04_09_06_date_20_08_2023_7.xml', 'marvel_6_time_10_24_03_date_19_08_2023_0.xml', 'marvel_6_time_10_24_03_date_19_08_2023_1.xml', 'marvel_6_time_10_24_03_date_19_08_2023_2.xml', 'marvel_6_time_10_24_03_date_19_08_2023_3.xml', 'marvel_6_time_10_24_03_date_19_08_2023_4.xml', 'marvel_6_time_10_24_03_date_19_08_2023_5.xml', 'marvel_6_time_10_24_03_date_19_08_2023_6.xml', 'marvel_8_time_09_09_04_date_27_08_2023_0.xml', 'marvel_8_time_09_09_04_date_27_08_2023_2.xml', 'marvel_8_time_09_09_04_date_27_08_2023_3.xml', 'marvel_8_time_09_09_04_date_27_08_2023_4.xml', 'marvel_8_time_09_09_04_date_27_08_2023_5.xml', 'marvel_8_time_09_09_04_date_27_08_2023_7.xml']

directories = ['marvel1_time_10_24_03_date_19_08_2023_0', 'marvel1_time_10_24_03_date_19_08_2023_1', 'marvel2_time_10_24_03_date_19_08_2023_0', 'marvel2_time_10_24_03_date_19_08_2023_1', 'marvel3_time_09_09_04_date_27_08_2023_0', 'marvel3_time_10_24_03_date_19_08_2023_0', 'marvel3_time_10_24_03_date_19_08_2023_1', 'marvel7_time_10_24_03_date_19_08_2023_0', 'marvel7_time_10_24_03_date_19_08_2023_1', 'marvel8_time_10_24_04_date_19_08_2023_0', 'marvel_1_time_04_09_04_date_20_08_2023_0', 'marvel_1_time_04_09_04_date_20_08_2023_3', 'marvel_1_time_04_09_04_date_20_08_2023_4', 'marvel_1_time_04_09_04_date_20_08_2023_5', 'marvel_1_time_04_09_04_date_20_08_2023_6', 'marvel_1_time_04_09_04_date_20_08_2023_7', 'marvel_3_time_04_09_06_date_20_08_2023_0', 'marvel_3_time_04_09_06_date_20_08_2023_1', 'marvel_3_time_04_09_06_date_20_08_2023_2', 'marvel_3_time_04_09_06_date_20_08_2023_3', 'marvel_3_time_04_09_06_date_20_08_2023_5', 'marvel_3_time_04_09_06_date_20_08_2023_7', 'marvel_6_time_10_24_03_date_19_08_2023_0', 'marvel_6_time_10_24_03_date_19_08_2023_1', 'marvel_6_time_10_24_03_date_19_08_2023_2', 'marvel_6_time_10_24_03_date_19_08_2023_3', 'marvel_6_time_10_24_03_date_19_08_2023_4', 'marvel_6_time_10_24_03_date_19_08_2023_5', 'marvel_6_time_10_24_03_date_19_08_2023_6', 'marvel_6_time_10_24_03_date_19_08_2023_7', 'marvel_8_time_09_09_04_date_27_08_2023_0', 'marvel_8_time_09_09_04_date_27_08_2023_2', 'marvel_8_time_09_09_04_date_27_08_2023_3', 'marvel_8_time_09_09_04_date_27_08_2023_4', 'marvel_8_time_09_09_04_date_27_08_2023_5', 'marvel_8_time_09_09_04_date_27_08_2023_7']

# Strip the .xml extension from xml_files and create a set
xml_files_stripped = {file[:-4] for file in xml_files}

# Convert directories list to a set for comparison
directories_set = set(directories)

# Find the missing directories
missing_directories = sorted(xml_files_stripped - directories_set)

print("Missing directories corresponding to XML files:")
for dir in missing_directories:
    print(dir)
