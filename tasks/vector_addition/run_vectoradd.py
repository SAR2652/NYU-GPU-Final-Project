import subprocess 
import socket

with open('vectoradd_raw_{}.csv'.format(socket.gethostname().split('.', 1)[0]), 'w') as f:
    for i in range(1,31):
        for num_blocks in range(1,17):
            for num_threads in range(1,11):
                result = subprocess.run(["./vectoradd.sh", str(2**(i)), str(num_blocks),str(2**num_threads)], stdout = subprocess.PIPE)
                content = result.stdout.decode('utf-8')
                items = content.split('\n')
                #print(items[0])
                #print(items[1])
                #speedup = float(items[0]) / float(items[1])
                f.write(','.join([str(i),str(num_blocks),str(num_threads), items[0]]) + '\n')
            
        print("Task {} completed ".format(i))
