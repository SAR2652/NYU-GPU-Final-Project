import sys, subprocess

args = sys.argv

file = args[1]

dims = int(input("Enter Dimension: "))
blocks = int(input("Enter the number of blocks: "))
threads = int(input("Enter the number of threads per block:"))

print("Please make sure that your argument file does not print anything except for the time taken for execution!")

exe = file.split('.')[0]

subprocess.run(["nvcc", "-o", exe, file])

result_st = subprocess.run(["./" + exe, str(dims), str(blocks), "1"], stdout = subprocess.PIPE)

content_st = result_st.stdout.decode('utf-8')

st_time = float(content_st.strip())

print("Time Taken for a Single Thread to execute for {} dimensions and {} blocks = {}".format(dims, blocks, st_time))

result = subprocess.run(["./" + exe, str(int), str(blocks), str(threads)], stdout = subprocess.PIPE)

content = result.stdout.decode('utf-8')

actual_time = float(content.strip())

print("Time Taken for a {} threads per block to execute for {} dimensions and {} blocks = {}".format(threads, dims, blocks, actual_time))

speedup = st_time / actual_time

print("Actual Speedup: {}".format(speedup))
