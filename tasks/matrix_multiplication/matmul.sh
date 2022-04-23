#!/bin/bash
nvcc -o matmul matmul.cu
./matmul $1 $2
