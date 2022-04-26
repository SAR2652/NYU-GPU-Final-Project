#include <stdio.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <cuda.h>
#include <math.h>

// Convenience function for checking CUDA runtime API results
// can be wrapped around any runtime API call. No-op in release builds.



__global__ void matSum(float* S, float* A, float* B, int N) {
  int j = blockIdx.y*blockDim.y + threadIdx.y;
  int i = blockIdx.x*blockDim.x + threadIdx.x;
  int tid = i*N + j;
  if (tid < N*N) {
    S[tid] = A[tid] + B[tid];
  }
}


// Fills a vector with random float entries.
void randomInit(float* data, int N) {
  for (int i = 0; i < N; ++i) {
    for (int j = 0; j < N; ++j) {
      int tid = i*N+j;
      data[tid] = (float)drand48();
    }
  }
}


int main(int argc, char* argv[])
{

//   if (argc != 3) {
//     // fprintf(stderr, "Syntax: %s <matrix size> <CacheConfL1>  <device> \n", argv[0]);
//     return EXIT_FAILURE;
//   }

  clock_t start, end; 
  int N = atoi(argv[1]);
  int Tile_Width = atoi(argv[3]);
  //int devId = atoi(argv[2]);

  //cudaDeviceReset();

  // set seed for drand48()
  srand48(42);

  // allocate host memory for matrices A and B
  float* A = (float*) malloc(N * N * sizeof(float));
  float* B = (float*) malloc(N * N * sizeof(float));
  float* S = (float*) malloc(N * N * sizeof(float));

  // initialize host matrices
  
  randomInit(A, N);
  randomInit(B, N);

  // allocate device matrices (linearized)
  float* dev_A = NULL; 
  float* dev_B = NULL;
  float* dev_S = NULL;
  cudaMalloc((void**) &dev_A, N * N * sizeof(float));
  cudaMalloc((void**) &dev_B, N * N * sizeof(float));
  cudaMalloc((void**) &dev_S, N * N * sizeof(float));

  // copy host memory to device
  cudaMemcpy(dev_A, A, N*N*sizeof(float), cudaMemcpyHostToDevice);
  cudaMemcpy(dev_B, B, N*N*sizeof(float), cudaMemcpyHostToDevice);

  // execute the kernel

  int GridSize = atoi(argv[2]);
  dim3 gridDim(GridSize, GridSize);
  dim3 blockDim(Tile_Width, Tile_Width);
  start = clock();
  matSum<<< gridDim, blockDim >>>(dev_S, dev_A, dev_B, N);
  end = clock();

  // copy result from device to host
  cudaMemcpy( S, dev_S, N * N * sizeof(float),cudaMemcpyDeviceToHost);

  //cudaDeviceProp prop;
  //cudaGetDeviceProperties(&prop, devId);
  //printf("Device: %s\n", prop.name);

  // clean up memory
  free(A);
  free(B);
  free(S);
  cudaFree(dev_A);
  cudaFree(dev_B);
  cudaFree(dev_S);
  printf("%.8f\n", (double)(end - start) / CLOCKS_PER_SEC);
  return 0;
}