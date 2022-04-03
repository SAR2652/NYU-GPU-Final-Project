import subprocess
import json

result = subprocess.run('./getDeviceProp.sh', stdout = subprocess.PIPE)

content = result.stdout.decode('utf-8')

lines = content.splitlines()
data = dict()

current_device = None

for line in lines:
    key, value = line.split('=')
    if key == 'Device ID':
        current_device = 'device:{}'.format(value)
        data[current_device] = dict()
    else:
        if any(c.isalpha() for c in value):
            data[current_device][key] = value
        else:
            data[current_device][key] = float(value)

json_object = json.dumps(data, indent = 4)

with open('gpu_details.json', 'w') as f:
    json.dump(json_object, f)