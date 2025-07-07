# 🧠 Using `torch.compile` with `torch.cuda.amp` for Mixed Precision on RTX 3070 Mobile

This guide demonstrates how to combine `torch.compile` with PyTorch's Automatic Mixed Precision (AMP) to achieve significant performance improvements in both inference and training workloads on RTX 3070 Mobile GPU.

## Assumes  PyTorch 2.0+ with cu127+, NVIDIA driver 456.38+
In my case (07.2025): PyTorch 2.7.1 with cu128, NVIDIA driver 576.80 (CUDA Version: 12.9)

---

## ⚙️ Inference or Embedding: (no GradScaler needed)

```python
import torch

# (1) compile once in full-precision
compiled_model = torch.compile(model, mode="max-autotune", fullgraph=False)

# (2) run inference under autocast - this casts eligible ops to fp16/bf16
with torch.cuda.amp.autocast(dtype=torch.float16):
    predictions = compiled_model(inputs)            # warm-up

# optional: persist the compiled kernels for faster startups next time
torch.compiler.save_cache_artifacts("rtx3070_cache")    # CUDA 2.7+ only
```

---

## 🏋️ Training or Finetuning: (add GradScaler)

```python
import torch
from torch.cuda.amp import autocast, GradScaler
# Mixed precision’s risk of underflow exists only when gradients propagate, so GradScaler is needed for training

# Compile the model
compiled_model = torch.compile(model, mode="max-autotune", fullgraph=False)

# Initialize the gradient scaler
scaler = GradScaler()                # guards fp16 grads

for inputs, labels in dataloader:
    optimizer.zero_grad(set_to_none=True)
    with autocast(dtype=torch.float16):
        outputs = compiled_model(inputs)
        loss = loss_function(outputs, labels)
    scaler.scale(loss).backward()   # backward in fp16
    scaler.step(optimizer)          # unscale + step
    scaler.update()                 # update scale factor
```

---

## 🔍 Key Considerations

* **Placement of `autocast`**: Ensure that `torch.compile` wraps the model before entering the `autocast` context. Placing `autocast` inside the compiled function can lead to graph breaks, reducing performance benefits.

* **Choosing `dtype`**:

  * `torch.float16`: Offers maximum speedups on Ampere GPUs like the RTX 3070 Mobile.
  * `torch.bfloat16`: Provides better numerical stability with slightly reduced performance.

* **Using `GradScaler`**: Essential during training to prevent gradient underflow, especially when using `float16`.

* **Saving Compiled Artifacts**: Utilize `torch.compiler.save_cache_artifacts()` to store compiled kernels, reducing startup time in subsequent runs.

---

## 📚 References

* [PyTorch Automatic Mixed Precision Tutorial](https://pytorch.org/tutorials/recipes/recipes/amp_recipe.html)
* [PyTorch `torch.compile` Documentation](https://pytorch.org/docs/stable/generated/torch.compile.html)

---