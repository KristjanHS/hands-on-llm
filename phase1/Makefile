<<<<<<< HEAD
.PHONY: venv keyring setup
=======
.PHONY: venv setup
>>>>>>> 80a4a47f2e26e5c6e8a5f657bb7c7089ac50ee9d

venv:
	python3 -m venv .venv

<<<<<<< HEAD
keyring:
	wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb
	sudo dpkg -i cuda-keyring_1.1-1_all.deb

setup:
	source .venv/bin/activate && \
	pip install --upgrade pip && \
	pip install torch==2.7.1 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128 && \
=======
setup:
	source .venv/bin/activate && \
	pip install --upgrade pip && \
	pip install torch==2.5.1+cu121 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121 && \
>>>>>>> 80a4a47f2e26e5c6e8a5f657bb7c7089ac50ee9d
	pip install -r requirements.txt
