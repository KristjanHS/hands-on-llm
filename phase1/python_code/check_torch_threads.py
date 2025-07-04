# This script checks the number of threads used by PyTorch.
# It is useful to verify that the number of threads is set correctly for performance tuning.
# It should match the number of CPU cores available on the system.
import os
import multiprocessing
import torch

# print(torch.__config__.show()) # Uncomment to see detailed PyTorch configuration

print("pytorch using physical CPU cores: ", torch.get_num_threads())

print("CPU threads (logical processors): ", os.cpu_count())
print("Physical cores: ", multiprocessing.cpu_count())
