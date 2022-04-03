import subprocess
import json

class GPUProfiler:
    def __init__(self):
        result = subprocess.run('./getDeviceProp.sh', stdout = subprocess.PIPE)
        self.content = result.stdout.decode('utf-8')
        self.data = None
    
    def getDevicePropDict(self):
        if self.data != None:
            return self.data
        lines = self.content.splitlines()
        self.data = dict()
        current_device = None
        for line in lines:
            key, value = line.split('=')
            if key == 'Device ID':
                current_device = 'device:{}'.format(value)
                self.data[current_device] = dict()
            else:
                if any(c.isalpha() for c in value):
                    self.data[current_device][key] = value
                else:
                    self.data[current_device][key] = float(value)

        return self.data

    def getDevicePropJSON(self):
        self.data = self.getDevicePropDict()
        return json.dumps(self.data, indent = 4)

    def saveAsJSON(self, filepath = 'gpu_details.json'):
        json_object = self.getDevicePropJSON()
        if filepath[-5:] != '.json':
            print('Incorrect File Extension!')
            return
        with open(filepath, 'w') as f:
            json.dump(json_object, f)

        print('JSON File saved as {}.'.format(filepath))