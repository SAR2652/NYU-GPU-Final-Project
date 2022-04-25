import sys, json, pickle
import numpy as np
import pandas as pd
from utils.utils import GPUProfiler

args = sys.argv

code_file = args[1]

data_point = []

gpu = GPUProfiler()
gpu_dict = gpu.getDevicePropDict()

dimensions = int(input("Enter dimensions of input: "))
blocks = int(input("Enter number of blocks: "))
threads = int(input("Enter number of threads: "))

data_point.append(dimensions)
data_point.append(blocks)
data_point.append(threads)

le = pickle.load(open('label_encoder.pickle', 'rb'))

gpu_le = le.transform(np.array([gpu_dict['Device Name']]).reshape(-1, 1))[0]

data_point.append(gpu_le)




