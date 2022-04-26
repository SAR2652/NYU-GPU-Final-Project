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

for key, value in gpu_dict.items():
    if key == 'Device Name':
        gpu_oe = oe.transform([gpu_dict['Device Name']])[0][0]
        data_point.append(gpu_oe)
    else:
        data_point.append(value)

"""Bag of Words Section"""
bow = BagOfWordsGenerator(code_file)
identity_dict = bow.getBOW()

for _, value in identity_dict:
    data_point.append(value)

rf_model = pickle.load(open('random_forest_model.pickle', 'rb'))

prediction = rf_model.predict([data_point])

print('Approximate Time taken by the code to execute will be {} seconds'.format(prediction[0][0]))
