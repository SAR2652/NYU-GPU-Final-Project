#!/bin/bash
nvcc -o vectorprog vectors.cu
./vectorprog $1 $2 $3