# This script checks the number of threads used by PyTorch.
# It is useful to verify that the number of threads is set correctly for performance tuning.
# It should match the number of CPU cores available on the system.
import torch
print(torch.get_num_threads())

import os
import multiprocessing

print("CPU threads (logical processors):", os.cpu_count())
print("Physical cores:", multiprocessing.cpu_count())