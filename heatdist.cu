/* 
 * This file contains the code for doing the heat distribution problem. 
 * You do not need to modify anything except starting  gpu_heat_dist() at the bottom
 * of this file.
 * In gpu_heat_dist() you can organize your data structure and the call to your
 * kernel(s), memory allocation, data movement, etc. 
 * 
 */

#include <cuda.h>
#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <math.h>

/* To index element (i,j) of a 2D array stored as 1D */
#define index(i, j, N)  ((i)*(N)) + (j)

/*****************************************************************/

// Function declarations: Feel free to add any functions you want.
void seq_heat_dist(float *, unsigned int, unsigned int);
void gpu_heat_dist(float *, unsigned int, unsigned int);
__global__ void heat_distribution_kernel(float*, float*, unsigned int);

/*****************************************************************/
/**** Do NOT CHANGE ANYTHING in main() function ******/

int main(int argc, char * argv[])
{
  unsigned int N; /* Dimention of NxN matrix */
  int type_of_device = 0; // CPU or GPU
  int iterations = 0;
  int i;
  
  /* The 2D array of points will be treated as 1D array of NxN elements */
  float * playground; 
  
  // to measure time taken by a specific part of the code 
  double time_taken;
  clock_t start, end;
  
  if(argc != 4)
  {
    fprintf(stderr, "usage: heatdist num  iterations  who\n");
    fprintf(stderr, "num = dimension of the square matrix (50 and up)\n");
    fprintf(stderr, "iterations = number of iterations till stopping (1 and up)\n");
    fprintf(stderr, "who = 0: sequential code on CPU, 1: GPU execution\n");
    exit(1);
  }
  
  type_of_device = atoi(argv[3]);
  N = (unsigned int) atoi(argv[1]);
  iterations = (unsigned int) atoi(argv[2]);
 
  
  /* Dynamically allocate NxN array of floats */
  playground = (float *)calloc(N*N, sizeof(float));
  if( !playground )
  {
   fprintf(stderr, " Cannot allocate the %u x %u array\n", N, N);
   exit(1);
  }
  
  /* Initialize it: calloc already initalized everything to 0 */
  // Edge elements  initialization
  for(i = 0; i < N; i++)
    playground[index(0,i,N)] = 100;
  for(i = 0; i < N-1; i++)
    playground[index(N-1,i,N)] = 150;

  if( !type_of_device ) // The CPU sequential version
  {  
    start = clock();
    seq_heat_dist(playground, N, iterations);
    end = clock();
  }
  else  // The GPU version
  {
     start = clock();
     gpu_heat_dist(playground, N, iterations); 
     end = clock();    
  }
  
  
  time_taken = ((double)(end - start))/ CLOCKS_PER_SEC;
  
  printf("Time taken for %s is %lf\n", type_of_device == 0? "CPU" : "GPU", time_taken);
  
  free(playground);
  
  return 0;

}


/*****************  The CPU sequential version (DO NOT CHANGE THAT) **************/
void  seq_heat_dist(float * playground, unsigned int N, unsigned int iterations)
{
  // Loop indices
  int i, j, k;
  int upper = N-1;
  
  // number of bytes to be copied between array temp and array playground
  unsigned int num_bytes = 0;
  
  float * temp; 
  /* Dynamically allocate another array for temp values */
  /* Dynamically allocate NxN array of floats */
  temp = (float *)calloc(N*N, sizeof(float));
  if( !temp )
  {
   fprintf(stderr, " Cannot allocate temp %u x %u array\n", N, N);
   exit(1);
  }
  
  num_bytes = N*N*sizeof(float);
  
  /* Copy initial array in temp */
  memcpy((void *)temp, (void *) playground, num_bytes);
  
  for( k = 0; k < iterations; k++)
  {
    /* Calculate new values and store them in temp */
    for(i = 1; i < upper; i++)
      for(j = 1; j < upper; j++)
	temp[index(i,j,N)] = (playground[index(i-1,j,N)] + 
	                      playground[index(i+1,j,N)] + 
			      playground[index(i,j-1,N)] + 
			      playground[index(i,j+1,N)])/4.0;
  
			      
   			      
    /* Move new values into old values */ 
    memcpy((void *)playground, (void *) temp, num_bytes);
  }

 // printf("Host Playground\n");
   // for(unsigned int i = 0; i < N; i++)
   // {
       // for(unsigned int j = 0; j < N; j++)
       // {
       //     printf("%f ", playground[index(i, j, N)]);
       // }
       // printf("\n");
    // }
  
}

/***************** The GPU version: Write your code here *********************/
/* This function can call one or more kernels if you want ********************/
void  gpu_heat_dist(float * playground, unsigned int N, unsigned int iterations)
{
    unsigned long long grid_count = pow(N, 2);
    unsigned long long alloc_size = grid_count * sizeof(float);
    float *device_playground, *intermediate_storage;

    cudaMalloc((void**) &device_playground, alloc_size);
    cudaMalloc((void**) &intermediate_storage, alloc_size);

    cudaMemcpy(device_playground, playground, alloc_size, cudaMemcpyHostToDevice);
    cudaMemcpy(intermediate_storage, playground, alloc_size, cudaMemcpyHostToDevice);

    unsigned int block_dim = 16;
    unsigned int grid_dim = ceil((double) N / block_dim);
    
    dim3 block_var(block_dim, block_dim, 1);
    dim3 grid_var(grid_dim, grid_dim, 1);

    for(unsigned int i = 0; i < iterations; i++)
    {
        heat_distribution_kernel<<<block_var, grid_var>>>(device_playground, intermediate_storage, N);
	cudaMemcpy(device_playground, intermediate_storage, alloc_size, cudaMemcpyDeviceToDevice);
    }

    cudaMemcpy(playground, device_playground, alloc_size, cudaMemcpyDeviceToHost);

    // printf("Device Playground\n");
    // for(unsigned int i = 0; i < N; i++)
    // {
       //  for(unsigned int j = 0; j < N; j++)
        // {
           //  printf("%f ", playground[index(i, j, N)]);
        // }
        // printf("\n");
    // }

    cudaFree(device_playground);
    cudaFree(intermediate_storage);
}

__global__ void heat_distribution_kernel(float* device_playground, float* intermediate_storage, unsigned int N)
{
    unsigned int i = blockIdx.x * blockDim.x + threadIdx.x;
    unsigned int j = blockIdx.y * blockDim.y + threadIdx.y;

    bool vertical_lower_limit = i >= 1;
    bool horizontal_lower_limit = j >= 1;
    bool vertical_upper_limit = i <= N - 2;
    bool horizontal_upper_limit = j <= N - 2;

    if(vertical_lower_limit && horizontal_lower_limit && horizontal_upper_limit && vertical_upper_limit)
    {
        intermediate_storage[index(i, j, N)] = device_playground[index(i - 1, j, N)] +
                                                device_playground[index(i, j - 1, N)] +
                                                device_playground[index(i + 1, j, N)] +
                                                device_playground[index(i, j + 1, N)];

        intermediate_storage[index(i, j, N)] /= 4.0;
    }
}


