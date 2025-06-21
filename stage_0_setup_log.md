# Stage 0 — WSL 2 + GPU Setup for LLM python development & First Experiments

This document distills **all meaningful commands** from my very first try‑everything session into a clear, replayable reference *and* a narrated journal.  
It replaces the raw, unfiltered `~/.bash_history` with something concise and educational.

> **Tip for future me:** every command block below can be copy‑pasted straight into a fresh WSL Ubuntu install to reproduce the same environment.

---

## Files in this Stage 0

| File | Purpose |
|------|---------|
| `test_WSL_Cuda_devicecount.cu` | Minimal CUDA program to count visible devices |
| `test_WSL_Cuda_devicecount` | Binary compiled from the above (should be `.gitignore`d) |
| `test_torch_gpu.py` | PyTorch `torch.cuda` test script |
| `test_jupyter_WSL_GPU.ipynb` | GPU test run from inside a Jupyter notebook |
| `test_vscode_jupyter.ipynb` | Integration test: Jupyter + VSCode kernel + GPU |
| `test_WSL_python_path.py` | Diagnostic of which Python interpreter is being used |
| `test_cwd_.py` | Current working directory test (used to verify paths inside notebooks or scripts) |
| `rich_panel.py` | Experiment with rich CLI output or rendering |
| `homedir_date.sh` | Snapshot: home directory listing with dates |
| `requirements.txt` | Snapshot of Python packages installed manually |
| `ready.txt` | Marker file or placeholder for workflow checkpoint |

These are exploratory, rough, and deliberately not yet organized into "final" code. They're meant to track the **first working probes** into Python, CUDA, and Jupyter integration on WSL.

---

## 0  Prerequisites

```bash
# Run as an admin PowerShell first (outside WSL) to make sure WSL features are on
# dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
# dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
# wsl --update        # latest kernel
# wsl --shutdown      # restart the WSL VM
```

---

## 1  System update & essential tools

```bash
sudo apt update && sudo apt upgrade -y        # bring Ubuntu up to date
sudo apt install -y   \
  git curl wget build-essential xclip htop software-properties-common \
  gnome-keyring
```

*Rationale:* a clean, patched base plus a few quality‑of‑life utilities (htop, xclip, etc.).

---

## 2  Workspace layout

```bash
mkdir -p ~/projects/phase0 ~/scratch           # keep experiments contained
cd ~/projects/phase0
```

`~/projects/phase0` is where all Stage 0 artefacts live.

---

## 3  Git + GitHub SSH setup

```bash
# configure identity (global, runs once per machine)
git config --global user.name  "myname"
git config --global user.email "mymame@gmail.com"

# generate a modern key and copy to clipboard for GitHub Settings → SSH Keys
ssh-keygen -t ed25519 -C "wsl‑laptop‑gpu"
xclip -sel clip < ~/.ssh/id_ed25519.pub       # copies key to Windows clipboard

# create + clone repo (private)
gh repo create phase0-check --private --clone
cd phase0-check
```

> *Key insight:* committing early, even messy work, preserves the learning path and builds good Git muscle memory.

---

## 4  Python 3.11 and virtual env

```bash
sudo add-apt-repository -y ppa:deadsnakes/ppa
sudo apt update
sudo apt install -y python3.11 python3.11-venv python3.11-distutils
python3.11 -m venv .venv
source .venv/bin/activate
python --version          # 3.11.x
pip install --upgrade pip rich ipykernel
```

Create a `.venv/` in‑repo (later excluded from Git) for experiments.

---

## 5  Initial Python sanity scripts

```bash
printf 'print("hello from python on ubuntu on WSL!")\n' > hello.py
python hello.py
```

---

## 6  CUDA 12.5 toolkit for WSL 2 (toolkit‑only!)

```bash
# NVIDIA WSL repository pin
wget https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-wsl-ubuntu.pin
sudo mv cuda-wsl-ubuntu.pin /etc/apt/preferences.d/cuda-repository-pin-600

# key + repo
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/3bf863cc.pub \
  | sudo tee /etc/apt/keyrings/cuda-archive-keyring.gpg > /dev/null

echo "deb [signed-by=/etc/apt/keyrings/cuda-archive-keyring.gpg] \
https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/ /" \
| sudo tee /etc/apt/sources.list.d/cuda-wsl.list

sudo apt update
sudo apt install -y cuda-toolkit-12-5   # never install cuda-drivers in WSL!

# put nvcc on PATH for this shell and future sessions
echo 'export PATH=/usr/local/cuda-12.5/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
nvcc --version
```

---

## 7  GPU driver & runtime sanity checks

```bash
/usr/lib/wsl/lib/nvidia-smi                 # should match Windows driver version
ldconfig -p | grep libcuda.so               # ONLY /usr/lib/wsl/lib paths
nvcc --version                              # confirms compiler present
```

*If any **`nvidia-driver-*`** packages appear in the next command, something is wrong:*

```bash
dpkg -l | grep -E 'nvidia-(dkms|driver|kernel|modules)'
```

---

## 8  PyTorch 2.5.1 + CUDA 12.1 wheels

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
python - <<'PY'
import torch, platform, os
print('PyTorch', torch.__version__)
print('CUDA available:', torch.cuda.is_available())
print('GPU:', torch.cuda.get_device_name(0))
PY
```

> Even though the wheel is tagged **cu121**, it’s forward‑compatible with the CUDA 12.5 runtime from the Windows driver.

---

## 9  Jupyter & VS Code integration

```bash
pip install notebook jupyterlab
python -m ipykernel install --user --name=wsl-cuda --display-name "Python 3 (WSL CUDA)"

# typical usage
jupyter notebook        # or: jupyter lab
```

In VS Code (Remote WSL), open `phase0-check`, create a notebook, and select the **Python 3 (WSL CUDA)** kernel.

---

## 10  First CUDA kernel (C++)

```bash
nvcc test_WSL_Cuda_devicecount.cu -o test_WSL_Cuda_devicecount
./test_WSL_Cuda_devicecount
```

Or inspect `test_WSL_Cuda_devicecount.cu` directly. It counts visible devices using CUDA C++.

---

## 11  Git housekeeping

```bash
# exclude large outputs & environments
cat <<'GIT' >> .gitignore
# binary & build artefacts
test_WSL_Cuda_devicecount
*.out
*.o
# Python caches
__pycache__/
*.pyc
# Jupyter scratch checkpoints
.ipynb_checkpoints/
# Virtualenvs
.venv/
GIT

git add .gitignore stage0_setup_log.md *.cu *.py *.ipynb *.sh requirements.txt
git commit -m "Stage 0 setup: WSL GPU, CUDA 12.5, PyTorch 2.5.1, first kernels and notebooks"
git push -u origin main
```

---

## 12  Where to go next

- Stage 1: automate rebuild via `Makefile` / `tox`
- Stage 2: small PyTorch model training and GPU monitoring (`nvidia-smi` load)
- Stage 3: HuggingFace Transformers + quantisation on RTX 3070 Laptop

---

### End of Stage 0

Everything above is now canonical history — messy in the real‑time log, but **clean, grouped, and explained** here.

