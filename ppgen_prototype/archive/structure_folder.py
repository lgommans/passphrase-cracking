import sys
import os
from subprocess import call
from subprocess import Popen
from subprocess import check_output
import subprocess

all_persons = check_output('ls ./q_raw', shell=True).strip().split()
dev_null = open(os.devnull, 'w')

for person in all_persons:
	file_path = './q_raw/' + person
	file_content = open(file_path).read().strip().split('\n')
	metadata_pair = file_content[0].split(',')
	metadata_check = file_content[0].split()
	if len(metadata_check) > 3:
		continue
	for meta_item in metadata_pair:
		if ' ' in meta_item:
			meta_item = meta_item.replace(' ', '_')
 		dir_name = './q_struct/' + meta_item
		if os.path.isdir(dir_name):
			call('cp ' + file_path + ' ' + dir_name, stdout=dev_null, stderr=subprocess.STDOUT, shell=True)
		else:
			print('dir created')
			call('mkdir ' + dir_name, stdout=dev_null, stderr=subprocess.STDOUT, shell=True)			
			call('cp ' + file_path + ' ' + dir_name, stdout=dev_null, stderr=subprocess.STDOUT, shell=True)

	
