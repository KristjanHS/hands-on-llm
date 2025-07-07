#!/usr/bin/env python3
import torch, xformers

print("Torch:", torch.__version__, torch.version.cuda)
print("xformers:", xformers.__version__)
print(
    "GPU visible:",
    torch.cuda.is_available(),
    torch.cuda.get_device_name(0) if torch.cuda.is_available() else "N/A",
)
print(torch.cuda.current_device())
