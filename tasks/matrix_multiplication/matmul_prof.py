import subprocess
import socket

result = subprocess.run("./matmul_prof.sh", stdout = subprocess.PIPE)

with open('matmul_prof_details.txt') as f:
    lines = f.readlines()
    lines = lines[3:]
    with open('matmul_prof_details_{}.csv'.format(socket.gethostname().split('.', 1)[0]), 'w') as f:
        for line in lines:
            f.write(line)

subprocess.run(["rm", "-r", "matmul_prof_details.txt"])