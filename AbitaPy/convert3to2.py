# script for translating the source code written
# in python3 from "sources" directory into a python2
# script into the "sources2" directory

import os
import shutil
import re
from lib3to2.main import main as convert3to2

SOURCE_DIR = "./abitaPy/"
DEST_DIR = "./abitaPy2/"

# remove the old files from python2 sources
print("Deleting files of previous version of abitaPy2...")
shutil.rmtree(DEST_DIR, ignore_errors=True)
print("Files deleted!")

# copy the python code
print("Copying the files of abitaPy...")
shutil.copytree(
    SOURCE_DIR,
    DEST_DIR,
    ignore=shutil.ignore_patterns("*[!(.py)]")
)
print("Files copied!")

# convert it
print("Converting sources from python3 to python2...")
convert3to2(
    fixer_pkg="lib3to2.fixes",
    args=["-wn", "--no-diffs", DEST_DIR]
)
print("Conversion terminated!")

# remove typing import because not compatible with ironpython
print("Removing the typing imports...")
list_of_files = []
for root, dirs, files in os.walk(DEST_DIR):
    for file in files:
        path = os.path.join(root, file)
        with open(path, 'r') as file_instance:
            data = file_instance.read()
            data = re.sub(r'from typing import .*\n', '', data)
        with open(path, 'w') as file_instance:
            file_instance.write(data)
print("Typing import removed!")

print("=================================")
print("=== CONVERSION TERMINATED !!! ===")
print("=================================")



