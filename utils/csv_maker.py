import os, re, sys, json
import numpy as np
import pandas as pd

args = sys.argv

task = args[1]
task_name = task.split('/')[1]
gpu_folder = args[2]    # GPU Info folder
bow_file = args[3]

raw_files = sorted([file for file in os.listdir(task) if 'raw' in file and file.endswith('.csv')])
prof_files = sorted([file for file in os.listdir(task) if 'prof' in file and file.endswith('.csv')])
gpu_info_files = sorted([file for file in os.listdir(gpu_folder)])

# Store DataFrames for Concatenation
result = []

for i in range(len(raw_files)):
    """Raw Computations File"""
    raw_file = os.path.join(task, raw_files[i])
    df = pd.read_csv(raw_file, names = ['Dimensions', 'Blocks', 'Threads', 'Time'], header = None)
    strs = df[['Dimensions', 'Threads', 'Time']][df['Threads'] == 1]
    indices = strs.index.tolist()

    speedup = df['Time'].tolist()
    times = df['Time'].tolist()
    count = 0
    
    for j in range(len(speedup)):
        if j > 0 and j in indices and count < len(indices) - 1:
            count += 1

        speedup[j] = times[indices[count]] / speedup[j]

    df['Speedup'] = np.array(speedup).T

    """Profiling File"""
    prof_file = os.path.join(task, prof_files[i])
    pf = pd.read_csv(prof_file)
    cols = ['Time', 'Avg', 'Min', 'Max', 'Name']
    pf = pf[cols]

    pf.dropna(inplace= True)

    relevant = ['[CUDA memcpy DtoH]', '[CUDA memcpy HtoD]', 'cudaMemcpy', 'cudaMalloc', 'cudaFree']

    dims = None
    for row in pf.values:
        if row[-1] in relevant:
            for j in range(len(cols[:-1])):
                if task_name == 'matrix_multiplication' or task_name == 'matrix_sum':
                    dims = 8192 * 8192
                elif task_name == 'vector_addition':
                    dims = 1000000
                df[row[-1] + ' ' + cols[j] + ' cost'] = np.array([float(row[j]) / dims * 1000] * df.shape[0]).T
    
    """GPU Details File"""
    gpu_file = os.path.join(gpu_folder, gpu_info_files[i])
    f = open(gpu_file).read()
    t = json.loads(f)
    gpu_dict = json.loads(t)
    for key, value in gpu_dict['device:0'].items():
        df[key] = np.array([value for i in range(df.shape[0])]).T

    """Bag of Words File"""
    f = open(bow_file)
    data = json.load(f)
    bow_dict = json.loads(data)

    for key, value in bow_dict.items():
        df[key] = np.array([value for i in range(df.shape[0])]).T

    result.append(df)
    print('Joined {}, {}, {} & {}'.format(raw_file, prof_file, gpu_file, bow_file))

filename = 'readings/{}_final.csv'.format(task_name)
final_df = pd.concat(result)
final_df.to_csv(filename, index = False)

print('Created {}!'.format(filename))