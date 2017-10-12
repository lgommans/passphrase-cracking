import subprocess

top_output = subprocess.check_output("top -n 1 -b", shell=True).strip().split('\n')
for line in top_output:
    print line
