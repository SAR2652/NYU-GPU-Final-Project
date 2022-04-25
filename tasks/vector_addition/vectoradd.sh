#!/bin/bash
nvcc -o vectorprog vectors.cu
# nvprof --csv --log-file vectoradd_prof_details.txt ./vectorprog $1 $2 $3
./vectorprog $1 $2 $3