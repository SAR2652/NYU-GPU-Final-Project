import os
import pandas as pd

folder = 'readings'

files = [file for file in os.listdir(folder)]

data = []

for file in files:
    temp = pd.read_csv(os.path.join(folder, file))
    data.append(temp)

df = pd.concat(data, axis = 1)

df.to_csv('final_data.csv', index = False)
