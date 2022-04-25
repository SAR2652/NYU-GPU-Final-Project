#!/bin/bash
nvcc -o vectorprog vectors.cu
nvprof --csv --log-file vectoradd_prof_details.txt ./vectorprog 1000000 8 128
