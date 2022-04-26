import os, subprocess, json, socket, shutil

class GPUProfiler:
    def __init__(self):
        proc = './getDeviceProp.sh'
        if 'getDeviceProp.sh' not in os.listdir():
            proc = './utils/getDeviceProp.sh'
        result = subprocess.run(proc, stdout = subprocess.PIPE)
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

class BagOfWordsGenerator:
    def __init__(self, filename):
        self.filename = filename
        self.taskname = self.filename.split('/')[-1].split('.')[0]
        self.all_identifiers = {
                    'float':0,
                    'unsigned_int':0,
                    'int':0,
                    'num_blocks':0,
                    'num_grid':0,
                    'threads':0,
                    "cudaMalloc":0,
                    'cudaMemcpy':0,
                    'cudaFree':0,
                    '+':0,
                    'for':0,
                    '-':0,
                    '*':0,
                    '/':0
                }
        # GPU identifiers
        self.all_kernel_identifier = {'+', 'for','-','*', '/'}
        
    def getBOW(self):
        self.target = self.taskname + '.txt'
        shutil.copyfile(self.filename, self.target)
        with open(self.target) as f:
            lines = f.readlines()

        for line in lines:
            x = line.split()
            for identity in x:
                for key, _ in self.all_identifiers.items():
                    if key in identity and key not in self.all_kernel_identifier: # exclude cpu for loops and operations
                        self.all_identifiers[key] += 1

        list_value = []
        list_global_list = []
        stri_pop = "}"

        for index,text in enumerate(lines): 
            if (text.startswith("__global__") and lines[index+1].startswith("{\n")):
                if(index+1 != len(lines)-1):
                    k = index + 1
                else:
                    break
            
                list_value.append(0)
                while(len(list_value)):
                    if( k == len(lines) - 1):
                        break
                    if(stri_pop in lines[k]):
                        list_value.pop()
                        list_global_list.append(lines[k])
                    if("{" in lines[k]):
                        list_value.append(0)
                    else:
                        list_global_list.append(lines[k])
                    k += 1
                
        for line in list_global_list:
            x = line.split()
            for identity in x:
                for key in self.all_kernel_identifier:
                    if key in identity: # count gpu for loops and operations
                        self.all_identifiers[key] += 1

        subprocess.run(["rm", self.target])
        return self.all_identifiers

    def saveJSON(self):
        all_identifiers = self.getBOW()
        vals = json.dumps(all_identifiers, indent = 4)
        with open('bow_files/bow_' + self.taskname + '.json', 'w') as f:
            json.dump(vals, f)



# class ParseTreeGenerator:
#     def __init__(self, filename: str):
#         result = subprocess.run(["clang", "-Xclang", "-ast-dump", "-fsyntax-only", filename], stdout = subprocess.PIPE)
#         self.content = result.stdout.decode('utf-8')

#     def getParseTreeString(self):
#         return self.content

#     def saveParseTreeText(self, filepath = 'parse_tree.txt'):
#         if filepath[-4:] != '.txt':
#             print('Incorrect File Extension!')
#             return
#         with open(filepath, 'w') as f:
#             f.write(self.content)
#         print('Saved Parse Tree as {}.'.format(filepath))

