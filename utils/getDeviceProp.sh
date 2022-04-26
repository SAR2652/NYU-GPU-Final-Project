#!/bin/bash
FILE=deviceQuery.cu
if test -f "$FILE"; then
    nvcc -o deviceQuery deviceQuery.cu
else
    nvcc -o deviceQuery ./utils/deviceQuery.cu
fi
./deviceQuery
rm deviceQuery