# NYU-GPU-Final-Project

This repository contains the code for our coursework project for the course **CSCI-GA 3033-025 Special Topics- GPU:Architecture and Programming** studied under Prof. Mohammad Zahran.

## Setup Instructions (CIMS)

To access NYU CIMS machines, open a terminal and type the following command:

```
ssh <net-id>@access.cims.nyu.edu
```

Once you are logged in you need to access a system with CUDA enabled GPU. To do so, type:

```
ssh cuda1
```

**Note:** Other socket names that can be accessed include *cuda2*, *cuda3*, *cuda4* and *cuda5*.

Clone this repository using the following command:<br>

```
git clone https://github.com/SAR2652/NYU-GPU-Final-Project.git
```

Once you have cloned this repository change directory into the repository folder using the following command:<br>
```
cd NYU-GPU-Final-Project
```

You need to now setup a virtual environment using either *pip* or *anaconda* to execute the code for the project. If you are on a CIMS machine, the steps for Anaconda are preferred since *pip* does not allow versions of Python higher than 3.6 to be installed. 

### Pip
To create a virtual environment using **pip** use the following commands:
```
pip3 install virtualenv
virtualenv <ENV_NAME>
source /<ENV_NAME>/bin/activate
pip3 install -r requirements.txt
```
### Anaconda/Miniconda

If you are on an NYU CIMS machine, then you need to first load the *anaconda* module using the ```module``` command. to load anaconda type the following command:<br>

 ```
 module load anaconda3
 ```

To create an environment using **Anaconda/Miniconda** use the following commands:
```
conda env create -f environment.yml
```

To activate the created environment type:

```
conda activate proj_env
```

If there is an issue in the output of the command then execute the following commands:

```
conda init
exit
```

Now log into the same system again and change directory to the repository using the following:

```
ssh cuda1
cd NYU-GPU-Final-Project
```

Try activating the environment again with the command:

```
conda activate proj_env
```

## Predictions/Inference:
The file ```inference.py``` is used to predict the speedup for a given file passed as an argument which contains CUDA C/C++ code. Predictions can be obtained using the following command:<br>
```
python inference.py /path/to/code/file
```

This code can be tested on our code for Matrix Sum using the below command:
```
python inference.py tasks/matrix_sum/matsum.cu
```

Sample Inputs:
1. Dimensions = 100
2. Number of Blocks = 4
3. Number of Threads per Block = 8

To verify against the actual value of speed up you can execute the code file using the following command:
**Note**: Make sure that your file prints NOTHING ELSE except the EXECUTION TIME.
```
python test/actual_speedup.py /path/to/code/file
```

In our case:
```
python test/actual_speedup.py tasks/matrix_sum/matsum.cu 
```

## Data Generation and Training
To generate a combined CSV for any task, the command is as follows: (Use ```python3``` instead of ```python``` on Unix based systems)<br>
```python utils/csv_maker.py /path/to/tasks/folder /path/to/gpu/details/folder/ /path/to/bow_file.json```<br>

An example for <b>Matrix Multiplication</b> is :<br>

```python utils/csv_maker.py tasks/matrix_multiplication gpu_info bow_files/bow_matmul.json```<br>

To concatenate the generated CSVs for all tasks a single large CSV file, use the ```final_datagen.py``` file as follows:<br>

```python final_datagen.py```


## File Structure Information

The folders in this repository and their description are listed below:
1. **bow_files**: It contains the bag of words representation of code used for training.
2. **gpu_info**: It contains JSON files of the details of the GPUs used to generate training data.
3. **readings**: It contains the files for each task that are generated after concatenation.
4. **tasks**: It contains folders named after the tasks used for training and the coed for those tasks.
5. **test**: It contains the file *actual_speedup.py* thjat can be used to obtain the execution speed of an unseen task.
6. **utils**: It contains code to obtain information about the GPU, create Bag of Word Representations and concatenate the raw data files obtained after simulations.
