import sys
import subprocess
import os
import time

# RUN AS: python2.7 ppgen_runner.py serv1.txt

dev_null = open(os.devnull, 'w')
surveys = open(sys.argv[1]).read().strip().split('=====')
popen_counter = 0

total_surveys = len(surveys)
print('Running a total of ' + str(total_surveys) + ' survey entries.')

for survey in surveys:
    survey_lines = survey.strip().split('\n')
    survey_id = survey_lines[0].strip()
    encoded_pp = survey_lines[1].strip()
    run_command = 'pypy ppgen.py ' + survey_id + ' ' + encoded_pp
    for seed_input in survey_lines[2:]:
        run_command += ' ' + seed_input.strip()
    time.sleep(1)

    while True:
        popen_counter = 0
        top_output = subprocess.check_output('top -n 1 -b', shell=True).strip().split('\n')
        for line in top_output:
            if 'pypy' in line:
                popen_counter += 1
        if popen_counter < 4:
            print('Started ' + survey_id)
            subprocess.Popen(run_command, stdout=dev_null, stderr=subprocess.STDOUT, shell=True)
            break
        else:
            time.sleep(5)

print('Started all processes')

