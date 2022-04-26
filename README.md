# NYU-GPU-Final-Project

To generate a combined CSV for any task, the command is as follows: (Use ```python3``` instead of ```python``` on Unix based systems)<br>
```python utils/csv_maker.py /path/to/tasks/folder /path/to/gpu/details/folder/ /path/to/bow_file.json```<br>

An example for <b>Matrix Multiplication</b> is :<br>

```python utils/csv_maker.py tasks/matrix_multiplication gpu_info bow_files/bow_matmul.json```<br>

To concatenate the generated CSVs for all tasks a single large CSV file, use the ```final_datagen.py``` file as follows:<br>

```python final_datagen.py```

The file ```inference.py``` is used to predict the speedup for a given filoe passed as an argument which contains CUDA C/C++ code. Predictions can be obtained using the following command:<br>
```python inference.py /path/to/code/file```<br>

To 