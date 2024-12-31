#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// CPU
void randomArray(float *cpu_arrayA, float *cpu_arrayB, unsigned long SQWIDTH) {
    srand((unsigned)time(NULL));
    for (unsigned long i = 0; i < SQWIDTH * SQWIDTH; ++i) {
        cpu_arrayA[i] = ((float)rand() / (float)(RAND_MAX)) * 100;
        cpu_arrayB[i] = ((float)rand() / (float)(RAND_MAX)) * 100;
    }
}

void printMatrix(float *matrix, unsigned long SQWIDTH, const char *name) {
    printf("%s:\n", name);
    for (unsigned long i = 0; i < SQWIDTH * SQWIDTH; i++) {
        printf("%.2f\t", matrix[i]);
        if ((i + 1) % SQWIDTH == 0) {
            printf("\n");
        }
    }
}

// GPU
__global__ void kernel_1t1e(float *A, float *B, float *C, unsigned long WIDTH) {
    int rowID = threadIdx.y + blockIdx.y * blockDim.y; // Row address
    int colID = threadIdx.x + blockIdx.x * blockDim.x; // Column Address
    int elemID;                                       // Element address

    if (rowID < WIDTH && colID < WIDTH) {
        elemID = colID + rowID * WIDTH;
        C[elemID] = A[elemID] + B[elemID];
    }
}

int main(int argc, char* argv[]) {
    // Memory specification
    unsigned long SQWIDTH = 4;  

    const size_t d_size = sizeof(float) * size_t(SQWIDTH * SQWIDTH);

    // Multiprocessing constants
    const dim3 threadsPerBlock(4, 4);  // Adjust thread configuration for the larger matrix
    const dim3 blocksPerGrid(1, 1);     // Adjust block configuration

    // CUDA TIME
    float ms;
    float avems = 0.0;
    cudaEvent_t start, end;

    // Initialize host matrices
    clock_t h_alloctime = clock();
    float *h_matA = (float *)malloc(SQWIDTH * SQWIDTH * sizeof(float));
    float *h_matB = (float *)malloc(SQWIDTH * SQWIDTH * sizeof(float));
    float *h_matC = (float *)malloc(SQWIDTH * SQWIDTH * sizeof(float));
    randomArray(h_matA, h_matB, SQWIDTH);
    float *d_matA, *d_matB, *d_matC;

    clock_t d_alloctime = clock();
    cudaMalloc((void **)&d_matA, d_size);
    cudaMalloc((void **)&d_matB, d_size);
    cudaMalloc((void **)&d_matC, d_size);
    cudaMemcpy(d_matA, h_matA, d_size, cudaMemcpyHostToDevice);
    cudaMemcpy(d_matB, h_matB, d_size, cudaMemcpyHostToDevice);

    // ELEMENT
    cudaEventCreate(&start);
    cudaEventCreate(&end);
    cudaEventRecord(start, 0);

    kernel_1t1e<<<blocksPerGrid, threadsPerBlock>>>(d_matA, d_matB, d_matC, SQWIDTH);

    cudaEventRecord(end, 0);
    cudaEventSynchronize(end);
    cudaEventElapsedTime(&ms, start, end);

    avems += ms;
    cudaMemcpy(h_matC, d_matC, d_size, cudaMemcpyDeviceToHost);

    cudaEventDestroy(start);
    cudaEventDestroy(end);

    printMatrix(h_matA, SQWIDTH, "Matrix A");
    printMatrix(h_matB, SQWIDTH, "Matrix B");
    printMatrix(h_matC, SQWIDTH, "Matrix C");

    cudaFree(d_matA);
    cudaFree(d_matB);
    cudaFree(d_matC);
    free(h_matA);
    free(h_matB);
    free(h_matC);

    return 0;
}