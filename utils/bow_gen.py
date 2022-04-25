import sys, shutil, subprocess, json
args = sys.argv

file_name = args[1]
target = args[1].split('/')[-1].split('.')[0] + '.txt'
shutil.copyfile(file_name, target)

with open(target) as f:
    lines = f.readlines()
    all_identifiers = {
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
all_kernel_identifier = {'+', 'for','-','*', '/'}

for line in lines :
    x = line.split()
    for identity in x:
        for key,values in all_identifiers.items():
            if key in identity and key not in all_kernel_identifier: # exclude cpu for loops and operations
                all_identifiers[key] += 1

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
            k+=1
                
for line in list_global_list:
    x = line.split()
    for identity in x:
        for key in all_kernel_identifier:
            if key in identity: # count gpu for loops and operations
                all_identifiers[key] += 1

subprocess.run(["rm", target])

vals = json.dumps(all_identifiers, indent = 4)
with open('bow_files/bow_' + args[1].split('/')[-1].split('.')[0] + '.json', 'w') as f:
    json.dump(vals, f)
