# Phase 1 — Local LLM Experimentation & Integration

This phase focuses on working with Large Language Models (LLMs) locally (and a little in Google Colab), exploring various frameworks, and understanding model deployment and interaction patterns.

## Directory Structure

```
phase1/
├── python_code/            # Python source files for LLM interactions
├── jupyter_notebooks/      # Local experimentation notebooks
├── colab_notebooks/        # Google Colab integration examples
├── bash_scripts/           # Utility scripts for model management
└── txt/                    # Sample text data for experiments
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

## Getting Started

1. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up Ollama or other local LLM hosting solution, like Oobabooga

3. Explore the notebooks in `jupyter_notebooks/` or `colab_notebooks/`

## Key Features

- **Local Model Deployment**: Run models on your own hardware
- **API Integration**: Multiple ways to interact with models
- **Performance Analysis**: Benchmarking and optimization tools
- **Interactive Examples**: Jupyter notebooks for hands-on learning

## Dependencies

Key requirements (see `requirements.txt` for full list):
- Python 3.11+
- PyTorch with CUDA support
- Jupyter/IPython
- Various LLM API clients

## Usage Examples

### Local API Interaction
```python
# Example from benchm_ollama_local_api_chat.py
from phase1.python_code.windows_ip_in_wsl import get_windows_host_ip
```

### Benchmarking
Various scripts in `python_code/` demonstrate different approaches to model benchmarking and performance analysis.

## Notes & Best Practices

- Always monitor GPU memory usage when running local models
- Consider using different models for different tasks
- Keep track of API response times and resource usage

---

For the initial environment setup, refer to [Phase 0](../phase0/).
