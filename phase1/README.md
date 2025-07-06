# Phase 1 — Local LLM Experimentation & AI‑assisted Coding

Phase 1 is where the fun really starts: you host **Large Language Models locally** (inside
WSL 2 **or** bare‑metal Linux), wire them into notebooks, VS Code and Colab tunnels, then
benchmark, profile and iterate.  Everything below is reproducible on a fresh machine and
is distilled from \~2 400 shell history lines.

> **Upstream:** Phase 0 delivered working NVIDIA drivers, CUDA 12.x and a verified
> PyTorch wheel.  *Do **that** first.*

---

## Directory layout

```text
phase1/
├── python_code/              # Python helpers, LangChain wrappers, benchmarks
├── jupyter_notebooks/        # Local Jupyter experiments
├── colab_notebooks/          # Colab -> local tunnel examples
├── batch_and_shell/          # *.sh, *.bat utilities
├── cuda/                     # .cu kernels & tests (e.g. devicecount)
├── bin/                      # Compiled CUDA or C helpers
└── tests/                    # pytest & flake8
```

## Key Components

### 1. Local LLM Integration
- Ollama API integration and benchmarking
- Local model hosting and inference
- API compatibility layers

### 2. Model Experimentation
- Various model architectures (Mistral-7B, etc.)
- Performance benchmarking
- Different hosting approaches

### 3. Python Tools & Libraries
- LLM API wrappers and utilities
- Helper functions for model interaction
- Benchmarking and tracing tools

### 4. Notebooks
- Interactive examples and tutorials
- Google Colab integration with local clients
- Performance analysis and visualization

### 5. Bash Scripts
- Utility scripts for model management
- Environment setup and configuration

### 6. Documentation
- Design notes and scratchpads
- Usage examples and best practices

## Key Features

- **Local Model Deployment**: Run models on your own hardware
- **API Integration**: Multiple ways to interact with models
- **Performance Analysis**: Benchmarking and optimization tools
- **Interactive Examples**: Jupyter notebooks for hands-on learning

## Dependencies

Key requirements (see `requirements.txt` for full list):
- Python 3.12+
- PyTorch with CUDA support
- Jupyter/IPython
- Various LLM API clients

---

For the initial environment setup, refer to [Phase 0](../phase0/).

# Details of Phase 1 — Local LLM Experimentation & AI‑assisted Coding

The rest of this document **condenses the sprawling `~/.bash_history` from Phase 1** into a tidy,
commented reference *and* a narrated engineering journal.

Relationship to Phase 0: 
* Phase 0 handled GPU drivers, CUDA 12.x and a verified PyTorch wheel.
* Phase 1 builds on top of that stack and moves into model hosting, benchmarking and IDE integration.


> **Why bother?**
> Re‑running the blocks below on a fresh Ubuntu (WSL 2 *or* bare metal) will recreate the
> exact environment I used while exploring local Large Language Models (LLMs), Colab
> tunnels, LangChain integrations and VS Code AI helpers — without crawling through
> 1 400‑plus bash history lines.

## 0  Prerequisites (system level)

```bash
sudo apt update && sudo apt install -y \
  git curl wget build-essential software-properties-common \
  python3.11 python3.11-venv locales
sudo locale-gen en_US.UTF-8 && sudo update-locale LANG=en_US.UTF-8
```

Set a sane locale early; several Python wheels barf on missing UTF‑8.

---

## 1  CUDA 12.5 toolkit inside WSL 2 (optional but recommended)

CUDA ≥12.5 drops the ancient 525 driver dependency and includes bug‑fixed `nvcc`.

```bash
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/3bf863cc.pub | \
  gpg --dearmor | sudo tee /etc/apt/keyrings/cuda-archive-keyring.gpg >/dev/null

cat <<'LIST' | sudo tee /etc/apt/sources.list.d/cuda-wsl.list
# CUDA 12.5 for WSL Ubuntu

deb [signed-by=/etc/apt/keyrings/cuda-archive-keyring.gpg] \
  https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/ /
LIST

sudo apt update
sudo apt install -y cuda-toolkit-12-5
```

Quick sanity checks:

```bash
nvcc --version        # prints 12.5.###
nvidia-smi            # sees the Windows host GPU
ldconfig -p | grep libcuda.so
```

If an older repo polluted `apt`, clean with:
`sudo rm /etc/apt/sources.list.d/cuda*.list /etc/apt/keyrings/cuda-archive-keyring.gpg`.

---

## 2  Python 3.12 & virtual environments

```bash
sudo add-apt-repository -y ppa:deadsnakes/ppa
sudo apt update && sudo apt install -y python3.12 python3.12-venv python3.12-dev
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 12

python3 --version        # 3.12.x
python3.12 -m venv .venv # project‑local env
source .venv/bin/activate
pip install --upgrade pip
```

---

## 3  Stable CUDA wheel stack (PyTorch 2.5.1 + cu121)

```bash
pip install torch==2.5.1+cu121 \
  torchvision==0.20.1+cu121 \
  torchaudio==2.5.1+cu121 \
  --index-url https://download.pytorch.org/whl/cu121

# Optional newer build once tested
# pip install torch==2.7.1 --index-url https://download.pytorch.org/whl/cu128
```

> **Tip:** pin the exact wheel URL; `pip` loves to "help" by upgrading to mismatched builds.

Extra speed‑ups:

```bash
pip install flash-attn --no-build-isolation
```

---

## 4  Local model servers

### 4.1 Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull mistral
ollama serve > ~/ollama.log 2>&1 &    # background daemon on :11434
```

Smoke test with LangChain:

```bash
pip install -U langchain-ollama
python - <<'PY'
from langchain_ollama import ChatOllama
llm = ChatOllama(model="mistral")
print(llm.invoke("Hello Phase 1"))
PY
```

### 4.2 Text‑Generation‑WebUI (Oobabooga)

```bash
git clone https://github.com/oobabooga/text-generation-webui.git \
  ~/text-gen-install/text-generation-webui
cd ~/text-gen-install/text-generation-webui
bash one_click_installer.sh --reinstall
./cmd_linux.sh               # UI on http://127.0.0.1:7860
```

Benchmarks live in `phase1/python_code/benchm_*` and compare throughput.

### 4.3 Docker images (headless)

```bash
docker run -p 11434:11434 mistral/mistral:latest  # full‑fat container
```

Good for quick tests without polluting the host env.

---

## 5  Building `llama.cpp` with CUDA backend (optional)

```bash
sudo apt install -y build-essential cmake git ninja-build pkg-config
cd ~/projects && git clone https://github.com/ggml-org/llama.cpp.git
cd llama.cpp && git pull      # ensure ≥ Feb‑2025 commit
cmake -S . -B build -DGGML_CUDA=ON -DCMAKE_CUDA_ARCHITECTURES=86
cmake --build build -j$(nproc)

# quick run
./build/bin/llama-cli -m tiny-stories-phi2.gguf -p "Hello" --n-gpu-layers 20
```

Copy `libllama.so` into WebUI if you need faster GGUF loading.

---

## 6  Jupyter & IPython kernels

```bash
pip install notebook ipykernel nbdime
python -m ipykernel install --user --name=wsl-cuda --display-name "Python 3 (WSL CUDA)"
nbdime config-git --enable          # diff notebooks nicely
```

Optional notebook server hardening lives in `~/.jupyter/jupyter_notebook_config.py`.

---

## 7  VS Code & Dev Tools

```bash
# Essential extensions
code --install-extension ms-python.python
code --install-extension GitHub.copilot
code --install-extension Continue.continue

# Copilot CLI inside WSL
gh extension install github/gh-copilot

# Formatting & linting
pip install black "black[jupyter]" flake8 pre-commit pytest
pre-commit install
```

`Continue` talking to local Ollama on Windows often beats WSL 2 latency. Benchmark.

---

## 8  Git hygiene & large‑file ignores

```bash
echo -e "models/\n*.gguf\n.venv/\nlogs/" >> .gitignore
pip install pre-commit && pre-commit install
```

Stash CUDA blobs (`*.so`, `*.out`) into `stage0/bin` or `phase1/bin` and keep the repo lean.

---

## 9  History & backup scripts

```bash
export HISTTIMEFORMAT="%F %T "
history > phase1_commands_with_timestamps.txt

mkdir -p ~/.bash_history_backups
cat <<'SH' > ~/backup_bash_history.sh
#!/usr/bin/env bash
cp ~/.bash_history \
  ~/.bash_history_backups/$(date +"%F_%H%M%S").bash_history
SH
chmod +x ~/backup_bash_history.sh
(crontab -l; echo "0 3 * * * ~/backup_bash_history.sh") | crontab -
```

---

## 10  Troubleshooting checklist

* `nvidia-smi` shows the GPU?  If not, update Windows host driver > 555.
* `nvcc --version` matches PyTorch CUDA (cu121 vs cu128).
* Mixed Torch/xformers builds?  `pip uninstall -y torch xformers` and reinstall pinned wheels.
* Ollama service stuck?  `systemctl status ollama`, `sudo systemctl stop ollama` then `ollama serve`.
* Port 11434 unreachable from Windows?  `ip addr show eth0`, then proxy via `netsh interface portproxy`.

---

## 11  End of Phase 1

You now own a reproducible, GPU‑accelerated playground for LLM research:
Ollama, Oobabooga, `llama.cpp`, Jupyter and VS Code are all one‐command
away.  Branch the repo, swap models, rewrite benchmarks — **without**
scavenging bash history ever again.
