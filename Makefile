# ----------- Makefile for phase0-check (Stage 0) -----------

# Python & environment
PYTHON := $(VENV)/bin/python
VENV := $(CURDIR)/.venv

# Default: help
.DEFAULT_GOAL := help

# ----------- Commands -----------

help:  ## Show available commands
	@grep -E '^[a-zA-Z_-]+:.*?##' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?##"}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

venv:  ## Create and activate virtual environment
	python3.11 -m venv $(VENV)
	$(VENV)/bin/pip install --upgrade pip
	$(VENV)/bin/pip install -r requirements.txt

check-venv:
	@test -d $(VENV) || (echo "❌ Virtual environment not found. Run \`make venv\` first." && exit 1)

gpu-check: check-venv  ## Run GPU availability test
	$(PYTHON) stage0/scripts/test_torch_gpu.py

python-path:  ## Print the detected Python path
	$(PYTHON) stage0/scripts/test_WSL_python_path.py

cuda-devicecount:  check-venv  ## Run compiled CUDA binary (detect device count)
	./stage0/bin/test_WSL_Cuda_devicecount

cuda-compile:  check-venv ## Recompile CUDA test binary
	nvcc phase0/cuda/test_WSL_Cuda_devicecount.cu -o stage0/bin/test_WSL_Cuda_devicecount

jupyter:  check-venv ## Start Jupyter Notebook server
	$(VENV)/bin/jupyter notebook

clean:  ## Remove compiled files and cache
	rm -rf __pycache__ */__pycache__ *.pyc *.o *.out
	rm -f stage0/bin/test_WSL_Cuda_devicecount

