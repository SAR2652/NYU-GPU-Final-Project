import subprocess
import socket

with open('matmul_raw_{}.csv'.format(socket.gethostname().split('.', 1)[0]), 'w') as f:
    for i in ["256 ", "512", "768","1024 ",
            "1280"  ,
            "1536"  ,
            "1792"  ,
            "2048"  ,
            "2304"  ,
            "2560"  ,
            "2816"  ,
            "3072"  ,
            "3328"  ,
            "3584"  ,
            "3840"  ,
            "4096"  ,
            "4352"  ,
            "4608"  ,
            "4864"  ,
            "5120"  ,
            "5376"  ,
            "5632"  ,
            "5888"  ,
            "6144"  ,
            "6400"  ,
            "6656"  ,
            "6912"  ,
            "7168"  ,
            "7424"  ,
            "7680"  ,
            "7936"  ,
            "8192"  ]:   # dimensions
        for tpb in range(11): # threads per block
            result = subprocess.run(["./matmul.sh", str(i), str(2 ** tpb),], stdout = subprocess.PIPE)
            content = result.stdout.decode('utf-8')
            items = content.split('\n')
            f.write(','.join([i,str(items[1]),str(tpb), items[0]]) + '\n')
            
        print("Task {} completed ".format(i))
