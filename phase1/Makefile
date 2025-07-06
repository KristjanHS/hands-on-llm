.PHONY: venv keyring setup

venv:
	python3 -m venv .venv

keyring:
	wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb
	sudo dpkg -i cuda-keyring_1.1-1_all.deb

setup:
	source .venv/bin/activate && \
	pip install --upgrade pip && \
	pip install torch==2.7.1 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128 && \
	pip install -r requirements.txt
