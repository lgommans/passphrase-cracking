import os
import sys
from subprocess import call
from subprocess import Popen
from subprocess import check_output
import subprocess


all_lines = open('./all_seeds.txt').read().strip().split('\n')

files_to_check = []
for line in all_lines:
    if not line == '':
        if line[0] == '.':
            call('python2.7 file_validity2.py ' + line, shell=True)
