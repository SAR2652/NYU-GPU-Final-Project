import os, json

folder = 'gpu_info'

files = [file for file in os.listdir(folder) if file.endswith('.json')]

dev_gpu_map = dict()

for file in files:
    filepath = os.path.join(folder, file)
    key = file.split('_')[-1].split('.')[0]
    f = open(filepath).read()
    t = json.loads(f)
    gpu_dict = json.loads(t)
    dev_gpu_map[key] = gpu_dict['device:0']['Device Name']

json_map = json.dumps(dev_gpu_map, indent = 4)

with open('utils/device_gpu_name_mapping.json', 'w') as f:
    json.dump(json_map, f)
