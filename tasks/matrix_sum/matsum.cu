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

// Allocates a matrix with random float entries.
void randomInit(float* data, int size) {
  for (int k = 0; k < size; ++k) {
     data[k] = (float)drand48();
  }
}

int main(int argc, char* argv[])
{
  clock_t start, end;

  int Width = atoi(argv[1]);
  int Tile_Width = atoi(argv[3]);
  //int devId = atoi(argv[3]);

  //checkCuda( cudaSetDevice(devId) );
  //cudaDeviceReset();

  // allocate host memory for matrices M and N
  float* M = (float*) malloc(Width * Width * sizeof(float));
  float* N = (float*) malloc(Width * Width * sizeof(float));
  float* P = (float*) malloc(Width * Width * sizeof(float));
  // set seed for drand48()
  srand48(42);

  // initialize host matrices
  randomInit(M, Width*Width);
  randomInit(N, Width*Width);

  // allocate device matrices (linearized)
  float* Md = NULL; 
  float* Nd = NULL;
  float* Pd = NULL;
  start = clock();

  cudaMalloc((void**) &Md, Width * Width * sizeof(float));
  cudaMalloc((void**) &Nd, Width * Width * sizeof(float));
  cudaMalloc((void**) &Pd, Width * Width * sizeof(float));

  // copy host memory to device
  cudaMemcpy(Md, M, Width*Width*sizeof(float), cudaMemcpyHostToDevice);
  cudaMemcpy(Nd, N, Width*Width*sizeof(float), cudaMemcpyHostToDevice);
  cudaMemcpy(Pd, P, Width*Width*sizeof(float), cudaMemcpyHostToDevice);

  // execute the kernel

  int GridSize = atoi(argv[2]);
  dim3 gridDim(GridSize, GridSize);
  dim3 blockDim(Tile_Width, Tile_Width);
  
  matSum<<< gridDim, blockDim >>>(Pd, Md, Nd, Width);

  // copy result from device to host
  cudaMemcpy(P, Pd, Width * Width * sizeof(float),cudaMemcpyDeviceToHost);

  // clean up memory  
  cudaFree(Md);
  cudaFree(Nd);
  cudaFree(Pd);

  end = clock();
  double time_taken = (double)(end - start) / CLOCKS_PER_SEC;
  printf("%.8f", time_taken);

  free(M);
  free(N);
  free(P);

  return 0;
}