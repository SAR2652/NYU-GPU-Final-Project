#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <cuda.h>
#include <math.h>

// Convenience function for checking CUDA runtime API results
// can be wrapped around any runtime API call. No-op in release builds


__global__ void matMul(float* Pd, float* Md, float* Nd, int Width, int Tile_Width) {
  float Pvalue = 0.0;

  int j = blockIdx.x * Tile_Width + threadIdx.x;
  int i = blockIdx.y * Tile_Width + threadIdx.y;
if (j < Width && i < Width) {
  for (int k = 0; k < Width; ++k) {
    Pvalue += Md[i * Width + k] * Nd[k * Width + j];
  }
}
  Pd[i * Width + j] = Pvalue;
}


// Allocates a matrix with random float entries.
void randomInit(float* data, int size) {
  for (int k = 0; k < size; ++k) {
     data[k] = (float)drand48();
  }
}

// void seq_mat_mul(float* M, float* N, float* P, int Width)
// {
//     for(int i = 0; i < Width; i++)
//     {
//         for(int j = 0; j < Width; j++)
//         {
//             for(int k = 0; k < Width; k++)
//             {
                
//             }
//         }
//     }
// }

int main(int argc, char* argv[])
{
  clock_t start, end;

  int Width = atoi(argv[1]);
  int Tile_Width = atoi(argv[2]);
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

  int GridSize = (Width + Tile_Width-1) / Tile_Width;
  dim3 gridDim(GridSize, GridSize);
  dim3 blockDim(Tile_Width, Tile_Width);
  
  matMul<<< gridDim, blockDim >>>(Pd, Md, Nd, Width,Tile_Width);

  // copy result from device to host
  cudaMemcpy(P, Pd, Width * Width * sizeof(float),cudaMemcpyDeviceToHost);

  // clean up memory  
  cudaFree(Md);
  cudaFree(Nd);
  cudaFree(Pd);

  end = clock();
  double time_taken = (double)(end - start) / CLOCKS_PER_SEC;
  printf("%lf\n%d\n", time_taken, GridSize);

  free(M);
  free(N);
  free(P);

  return 0;
}
