import os, re, sys, json
import numpy as np
import pandas as pd

args = sys.argv

df = pd.read_csv(args[1])   # task speedup file
task = args[1].split('/')[1].split('_')[0]


if '.csv' in task:
    task = re.sub(r'\.csv', '', task)

df.columns = ['Dimensions', 'Blocks', 'Threads', 'Time']

strs = df[['Dimensions', 'Threads', 'Time']][df['Threads'] == 1]
indices = strs.index.tolist()

# In[31]:


speedup = df['Time'].tolist()
times = df['Time'].tolist()
count = 0
for i in range(len(speedup)):
    if i > 0 and i % 11 == 0:
        count += 1
    speedup[i] /= times[indices[count]]

df['Speedup'] = np.array(speedup).T

f = open(args[2])    # GPU Info file
data = json.load(f)
gpu_dict = json.loads(data)

device_name = None

for key, value in gpu_dict['device:0'].items():
    if key == 'Device Name':
        temp = value.split(' ')
        device_name = '_'.join(temp)
    df[key] = np.array([value for i in range(df.shape[0])]).T

f = open(args[3])  # bag of words file
data = json.load(f)
bow_dict = json.loads(data)

for key, value in bow_dict.items():
    df[key] = np.array([value for i in range(df.shape[0])]).T

filename = 'readings/{}_{}_final.csv'.format(task, device_name)

df.to_csv(filename, index = False)

print('Created {}!'.format(filename))