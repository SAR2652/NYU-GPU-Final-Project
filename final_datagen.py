import os
import pandas as pd

folder = 'readings'

files = [file for file in os.listdir(folder) if file.endswith('.csv')]

data = []

for file in files:
    temp = pd.read_csv(os.path.join(folder, file))
    data.append(temp)

df = pd.concat(data)

df.to_csv('final_data.csv', index = False)
