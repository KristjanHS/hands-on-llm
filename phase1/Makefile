.PHONY: venv setup

venv:
	python3 -m venv .venv

setup:
	source .venv/bin/activate && \
	pip install --upgrade pip && \
	pip install torch==2.5.1+cu121 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121 && \
	pip install -r requirements.txt
