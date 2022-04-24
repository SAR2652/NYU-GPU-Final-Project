import sys, shutil, subprocess, json
args = sys.argv

file_name = args[1]
target = args[1].split('/')[1].split('.')[0] + '.txt'
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
        'cudaFree':0
        }

for line in lines :
    x = line.split()
    for identity in x:
        for key,values in all_identifiers.items():
            if key in identity:
                all_identifiers[key] += 1

subprocess.run(["rm", target])

vals = json.dumps(all_identifiers, indent = 4)
with open('bow_files/bow_' + args[1].split('.')[0] + '.json', 'w') as f:
    json.dump(vals, f)
