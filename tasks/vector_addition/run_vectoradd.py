import subprocess, socket

with open('vectoradd_raw_{}.csv'.format(socket.gethostname().split('.', 1)[0]), 'w') as f:
    for i in range(1,7):
        for num_blocks in range(1,17):
            for num_threads in range(0,11):
                result = subprocess.run(["./vectoradd.sh", str(10**(i)), str(num_blocks),str(2**num_threads)], stdout = subprocess.PIPE)
                # subprocess.run(["./vectoradd.sh", str(10**(i)), str(num_blocks),str(2**num_threads)])
                # with open('vectoradd_prof_details.txt') as t:
                #     lines = t.readlines()
                #     lines = lines[5:]
                #     irrelevant = ["[CUDA memcpy HtoD]", "[CUDA memcpy DtoH]", "cudaMalloc", "cuDeviceGetAttribute", "cuDeviceTotalMem", "cudaMemcpy", "cuDeviceGetName", "cudaFree", "cudaLaunchKernel", "cuDeviceGetPCIBusId", "cuDeviceGet", "cuDeviceGetCount", "cuDeviceGetUuid"]
                #     time_taken = None
                #     for line in lines:
                #         items = line.split(',')
                #         if items[-1] not in irrelevant:
                #             time_taken = items[-4]
                #             break
                    # print(time_taken)

                # subprocess.run(["rm", "-r", "vectoradd_prof_details.txt"])
                content = result.stdout.decode('utf-8').strip()
                #print(items[0])
                #print(items[1])
                #speedup = float(items[0]) / float(items[1])
                f.write(','.join([str(10 ** i),str(num_blocks),str(2 ** num_threads), content]) + '\n')
            
        print("Task {} completed ".format(i))
