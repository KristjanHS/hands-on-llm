#!/usr/bin/env python3
import torch

# import xformers
# print("xformers:", xformers.__version__)

print("Torch:", torch.__version__, torch.version.cuda)
print(
    "GPU visible:",
    torch.cuda.is_available(),
    torch.cuda.get_device_name(0) if torch.cuda.is_available() else "N/A",
)

print("CUDA current device:", torch.cuda.current_device())
