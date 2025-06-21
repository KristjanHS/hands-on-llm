| Command                 | Does This                                               |
| ----------------------- | ------------------------------------------------------- |
| `make` or `make help`   | Shows all available tasks                               |
| `make venv`             | Creates a virtual environment and installs dependencies |
| `make gpu-check`        | Runs your PyTorch CUDA test script                      |
| `make python-path`      | Runs your Python path checker                           |
| `make cuda-compile`     | Compiles your `.cu` file with `nvcc`                    |
| `make cuda-devicecount` | Executes the compiled CUDA binary                       |
| `make jupyter`          | Launches Jupyter Notebook with your venv kernel         |
| `make clean`            | Cleans up cruft and build artefacts                     |
