import time
import torch


def benchmark_matmul():
    a = torch.randn(5000, 5000)
    b = torch.randn(5000, 5000)
    start = time.time()
    c = a @ b
    torch.cuda.synchronize() if torch.cuda.is_available() else None
    print(f"Elapsed: {time.time() - start:.3f} s")


torch.set_num_threads(6)
benchmark_matmul()

torch.set_num_threads(8)
benchmark_matmul()
