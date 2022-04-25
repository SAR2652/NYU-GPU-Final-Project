import subprocess, json, socket

class GPUProfiler:
    def __init__(self):
        result = subprocess.run('./getDeviceProp.sh', stdout = subprocess.PIPE)
        self.content = result.stdout.decode('utf-8')
        self.data = None
        self.device_name = socket.gethostname().split('.', 1)[0]
    
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

    def saveAsJSON(self):
        filepath = 'gpu_details_{}.json'.format(self.device_name)
        json_object = self.getDevicePropJSON()
        if filepath[-5:] != '.json':
            print('Incorrect File Extension!')
            return
        with open(filepath, 'w') as f:
            json.dump(json_object, f)

        print('JSON File saved as {}.'.format(filepath))

class ParseTreeGenerator:
    def __init__(self, filename: str):
        result = subprocess.run(["clang", "-Xclang", "-ast-dump", "-fsyntax-only", filename], stdout = subprocess.PIPE)
        self.content = result.stdout.decode('utf-8')

    def getParseTreeString(self):
        return self.content

    def saveParseTreeText(self, filepath = 'parse_tree.txt'):
        if filepath[-4:] != '.txt':
            print('Incorrect File Extension!')
            return
        with open(filepath, 'w') as f:
            f.write(self.content)
        print('Saved Parse Tree as {}.'.format(filepath))

