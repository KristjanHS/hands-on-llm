# 🚀 My Hands-On LLM Learning Journey

This repository tracks my hands-on learning journey with Large Language Models (LLMs) and Small Language Models (SLM), focusing on practical implementation and experimentation. Each phase builds upon the previous one, creating a comprehensive understanding of LLM development from environment setup to AI related projects (Python, notebooks, RAG, AI safety, ...).

## 🧭 Phases

### ✅ [Phase 0](./phase0/)
> *Goal:* Set up robust development environment (WSL2 + Python + CUDA + PyTorch GPU)
- Complete WSL2 configuration with GPU support
- Python 3.11 environment setup
- VScode IDE setup + github, copilot, WSL 2 venv
- CUDA toolkit and PyTorch integration
- Jupyter notebook first tests on local GPU
- Basic GPU validation tests via shell

### ✅ [Phase 1](./phase1/)
> *Goal:* Local LLM experimentation and integration, incl AI assisted coding
- Interactive notebooks (Colab+Ngrok, GitHub Codespaces) and examples to get started with Python for AI
- API integrations for various endpoints, both local and remote (local PC to colab)
- Local model deployment (Ollama and Oobabooga - both tried in Windows 10 and inside WSL 2 (ubuntu))
- Performance analysis and optimization (It turned out the Windows Ollama is fastest of my 4 local alternative setups)
- AI assisted coding in VSCode: trying out Copilot, Gemini Code Assist, and Continue (on local AI models, instead of API to cloud AI)

MY NEXT STEPs PLAN:

### ✅ [Phase 2](./phase2/)
> *Goal:* Local RAG experimentation and integration
- Trying out multiple local RAG architectures

### ✅ [Phase 3](./phase3/)
> *Goal:* AI safety topics + AI training & quantisation experimentation
- Trying out multiple AI safety related frameworks and approaches
- small PyTorch model training and GPU monitoring (`nvidia-smi` load)
- HuggingFace Transformers + quantisation


### 🔜 Future Phases
> Planning in progress...

## 🛠 Key Features

- **WSL2 + GPU Integration**: Optimized for Windows development with Linux tools
- **Local LLM Focus**: Run and experiment with models on your own hardware
- **Comprehensive Documentation**: Clear setup instructions and examples
- **Performance Analysis**: Benchmarking and optimization tools
- **Interactive Learning**: Jupyter notebooks for hands-on experimentation

## 📌 Why This Exists

This repository serves as both a learning journal and a practical reference for LLM development.
It demonstrates:
- Setting up a robust development environment
- Working with local LLM deployments
- Understanding model behavior and performance
- Practical implementation patterns and best practices

The goal is to provide a clear path from initial setup to advanced LLM applications, with each phase building upon previous knowledge.
