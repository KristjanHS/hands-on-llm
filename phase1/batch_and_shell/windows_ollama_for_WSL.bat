@echo off
set OMP_NUM_THREADS=8
set MKL_NUM_THREADS=8

set OLLAMA_NUM_PARALLEL=1
set OLLAMA_NUM_THREADS=8  # aga tundub et seda ignoreeritakse
set OLLAMA_KV_CACHE_TYPE=heap
set OLLAMA_CONTEXT_LENGTH=8192
set OLLAMA_HOST=0.0.0.0
ollama serve