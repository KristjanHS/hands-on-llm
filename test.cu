#include <cuda_runtime.h>
#include <iostream>
int main() {
  int count;
  cudaError_t err = cudaGetDeviceCount(&count);
  if (err != cudaSuccess) {
    std::cerr << "CUDA error: " << cudaGetErrorString(err) << "\n";
    return 1;
  }
  std::cout << "Number of CUDA devices: " << count << "\n";
}
