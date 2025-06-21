# tests/test_torch_gpu.py
import torch

def test_cuda_available():
    assert torch.cuda.is_available()
