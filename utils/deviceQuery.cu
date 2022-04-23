#include <cuda.h>
#include <stdlib.h>
#include <stdio.h>
#include <cuda_profiler_api.h>

int main()
{
  cudaError_t error;
  cudaDeviceProp dev;
  int dev_cnt = 0;

cudaProfilerStart();
  // return device numbers with compute capability >= 1.0
  error = cudaGetDeviceCount (&dev_cnt);
  if(error != cudaSuccess)
  {
    printf("Error: %s\n", cudaGetErrorString(error));
    exit(-1);
  }

  // Get properties of each device
  for(int i = 0; i < dev_cnt; i++)
  {
     error = cudaGetDeviceProperties(&dev, i);
     if(error != cudaSuccess)
     {
        printf("Error: %s\n", cudaGetErrorString(error));
        exit(-1);
     }
     printf("Device ID=%d\n", i);
     printf("Device Name=%s\n",dev.name);
     printf("Compute Capability=%d.%d\n",dev.major, dev.minor);
     printf("Total Global Memory=%ld\n", dev.totalGlobalMem/1024);
     printf("Shared Memory per Block=%d\n",dev.sharedMemPerBlock);
     printf("Registers per Block=%d\n", dev.regsPerBlock);
     printf("Warp Size=%d\n", dev.warpSize);
     printf("Maximum Threads per Block=%d\n",dev.maxThreadsPerBlock);
     printf("Thread Dimension Z=%d\n", dev.maxThreadsDim[0]);
     printf("Thread Dimension Y=%d\n", dev.maxThreadsDim[1]);
     printf("Thread Dimension X=%d\n", dev.maxThreadsDim[2]);
     printf("Grid Size Z=%d\n", dev.maxGridSize[2]);
     printf("Grid Size Y=%d\n", dev.maxGridSize[1]);
     printf("Grid Size X=%d\n", dev.maxGridSize[0]);
     printf("Clock Rate=%d\n",dev.clockRate);
     printf("Total Constant Memory=%ld\n",dev.totalConstMem);
     printf("Multiprocessor Count=%d\n",dev.multiProcessorCount);
     printf("integrated=%d\n",dev.integrated);
     printf("Asynchronous Engine Count=%d\n",dev.asyncEngineCount);
     printf("Memory Bus Width=%d\n",dev.memoryBusWidth);
     printf("Memory Clock Rate=%d\n",dev.memoryClockRate);
     printf("L2 Cache Size=%d\n", dev.l2CacheSize);
     printf("Maximum Threads per Multiprocessor=%d\n", dev.maxThreadsPerMultiProcessor);
     printf("Concurrent Kernels=%d\n", dev.concurrentKernels);
  }

cudaProfilerStop();
  return 0;

}
