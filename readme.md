# Stage 0 — WSL GPU Setup & First Experiments

Welcome to **Stage 0** of my GPU development journey. This stage captures my exploratory setup of a full NVIDIA GPU development environment on **Windows Subsystem for Linux 2 (WSL2)**, using:

- **Ubuntu 22.04 (WSL2)**
- **CUDA 12.5 Toolkit** (installed toolkit-only, no Linux drivers)
- **NVIDIA Driver 576.80** on Windows (CUDA 12.9 runtime)
- **PyTorch 2.5.1 with CUDA 12.1 wheel**
- **Jupyter + VSCode integration**
- **NVIDIA GeForce RTX 3070 Laptop GPU**

This is not production code — it's a documented sandbox for learning how CUDA, PyTorch, WSL, and Jupyter work together.

---

## 🌱 Goals

- Verify NVIDIA GPU visibility in WSL2
- Set up and test CUDA compilation (nvcc)
- Validate PyTorch GPU runtime access
- Get Jupyter working with GPU-aware kernels
- Organize chaotic exploration into a reproducible foundation

---

## 📁 Key Files in This Stage

| File                           | Description                                                        |
|--------------------------------|--------------------------------------------------------------------|
| `test_WSL_Cuda_devicecount.cu` | CUDA C++ program that reports number of visible GPUs              |
| `test_WSL_Cuda_devicecount`    | Compiled binary from above — ignored via `.gitignore`             |
| `test_torch_gpu.py`            | Minimal PyTorch `torch.cuda` check                                |
| `test_jupyter_WSL_GPU.ipynb`   | Same check, run in Jupyter                                        |
| `test_vscode_jupyter.ipynb`    | Notebook tested inside VSCode                                     |
| `test_WSL_python_path.py`      | Inspect active interpreter paths                                  |
| `test_cwd_.py`                 | Prints working directory — for debugging execution context        |
| `rich_panel.py`                | First play with Python `rich` library                             |
| `homedir_date.sh`              | Shell snapshot of home directory at setup time                    |
| `requirements.txt`             | Python packages used in this phase                                |
| `ready.txt`                    | Placeholder/checkpoint artifact                                   |
| `stage0_setup_log.md`          | Fully annotated and grouped command history for reproducing setup |

---

## 📚 Getting Started

To replay the full environment setup from scratch:

1. Clone this repo inside a WSL2 Ubuntu environment
2. Open and follow `stage0_setup_log.md`
3. Run each step incrementally (or adapt into a script)
4. Try running:

```bash
nvcc test_WSL_Cuda_devicecount.cu -o test_WSL_Cuda_devicecount
./test_WSL_Cuda_devicecount
```

Or test PyTorch:

```bash
python test_torch_gpu.py
```

---

## 🛣️ What’s Next

- **Stage 1** → Structure a proper project layout, `Makefile`, and test harness
- **Stage 2** → Run small PyTorch models and monitor GPU usage
- **Stage 3** → Load HuggingFace Transformers and explore quantization

---

## 🧠 Why I’m keeping this

This stage captures the exact mess, friction, and breakthrough moments I went through in building my first GPU setup on WSL2. It’s not just a checklist — it’s the **record of figuring things out**.

> Future me (or anyone following): feel free to laugh at the filenames — but appreciate the progress.

---

✍️ *Created by Kristjan Sillmann — Stage 0 complete.*

