#!/bin/bash
nvprof --csv --log-file matmul_prof_details.txt ./matmul 8192 128