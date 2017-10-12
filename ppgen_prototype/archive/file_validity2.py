
import sys
import os

for file_path in sys.argv[1:]:
    if not os.path.isfile(file_path):
        print(file_path)


