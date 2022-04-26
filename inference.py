import os, sys, json, pickle, socket
import numpy as np
import pandas as pd
from utils.utils import GPUProfiler, BagOfWordsGenerator

args = sys.argv

code_file = None

code_file = args[1]

if code_file == None:
    print("No code file specified!")

data_point = []

"""User Input Section"""
dimensions = int(input("Enter dimensions of input: "))
blocks = int(input("Enter number of blocks: "))
threads = int(input("Enter number of threads: "))

data_point.append(dimensions)
data_point.append(blocks)
data_point.append(threads)

"""Execution GPU Profiling Section"""
socket_name = socket.gethostname().split('.', 1)[0]

with open('utils/device_gpu_name_mapping.json') as f:
    content = f.read()
    temp = json.loads(content)
    map_dict = json.loads(temp)
    
if socket_name not in map_dict:
    socket_name = 'cuda5'
    print('Socket name not recognized! Using default profiling features (same as cuda5)...')

prof_path = 'tasks/vector_addition'

prof_files = os.listdir(prof_path)

prof_file = None

for file in prof_files:
    if 'prof_details_' + socket_name in file:
        prof_file = file
        break

prof_filepath = os.path.join(prof_path, prof_file)

profiling_features = ['[CUDA memcpy HtoD]', '[CUDA memcpy DtoH]', 'cudaMalloc', 'cudaMemcpy', 'cudaFree']

df = pd.read_csv(prof_filepath)

prof_details = df.values
names = df['Name'].tolist()

for feature in profiling_features:
    i = names.index(feature)
    for item in prof_details[i][-4:-1]:
        data_point.append(item)

"""Execution GPU Section"""
gpu = GPUProfiler()
gpu_dict = gpu.getDevicePropDict()
oe = pickle.load(open('utils/gpu_encoder.pickle', 'rb'))

gpu_details = gpu_dict['device:0']

for key, value in gpu_details.items():
    if key == 'Device Name':
        gpu_oe = oe.transform([[gpu_details['Device Name']]])[0][0]
        data_point.append(gpu_oe)
    else:
        data_point.append(value)

"""Bag of Words Section"""
bow = BagOfWordsGenerator(code_file)
identity_dict = bow.getBOW()

for _, value in identity_dict.items():
    data_point.append(value)

sc = pickle.load(open('utils/min_max_scaler.pickle', 'rb'))
rf_model = pickle.load(open('random_forest_model.pickle', 'rb'))

# print(data_point)

dp = sc.transform(np.array(data_point).reshape(1, -1))

prediction = rf_model.predict(dp)

print('Approximate Speedup Ratio w.r.t a single thread will be {}'.format(prediction[0]))
