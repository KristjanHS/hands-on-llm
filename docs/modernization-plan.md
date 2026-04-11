# Modernization Plan: hands-on-llm

**Created**: 2026-04-11
**Status**: Draft

---

## Phase 1: Security & Hygiene (Do First — All Tasks Independent)

### Task 1.1: Rotate Exposed Secrets

**Why**: `.env` files contain real API keys (Gemini, Nomic) and Weaviate password on disk. Not committed to git, but should be rotated as precaution.

**Steps**:
1. Rotate Gemini API key in `.env`
2. Rotate Nomic API key in `phase2/.env`
3. Change Weaviate password in `phase2/.env`
4. Update local `.env` files with new values

**Files affected**: None in repo (external service rotation).

### Task 1.2: Add .env.example Templates

**Why**: No documentation of which env vars are needed.

**Steps**:
1. Create `.env.example`:
   ```
   PYTHONPATH=.
   GEMINI_API_KEY=your-gemini-api-key-here
   ```
2. Create `phase2/.env.example`:
   ```
   NOMIC_API_KEY=your-nomic-api-key-here
   WEAVIATE_USER=your-email@example.com
   WEAVIATE_PASSWORD=your-weaviate-password
   COMPOSE_PROJECT_NAME=text2vec-weaviate
   ```
3. Add `!.env.example` to `.gitignore` after the `.env` line.

**Files to create**: `.env.example`, `phase2/.env.example`
**Files to modify**: `.gitignore`

### Task 1.3: Harden .gitignore Against Accidental Large-File Commits

**Why**: Defense-in-depth — even if `data/` pattern is removed from `.gitignore`, individual file patterns catch PDFs and model weights.

**Steps**:
1. Add to `.gitignore`:
   ```
   # Binary artifacts & model weights
   *.pdf
   *.pkl
   *.bin
   *.h5
   *.safetensors
   *.onnx
   ```

**Files to modify**: `.gitignore`

### Task 1.4: Delete Old/Backup Files From Git

**Why**: 4 explicitly superseded files + 1 exact byte-for-byte duplicate tracked in git.

**Steps**:
1. `git rm phase1/python_code/helper_functions_old.py`
2. `git rm phase2/python_PoC_scripts/ingest_pdf_old.py`
3. `git rm phase2/python_PoC_scripts/rag_weaviate_v2_old.py`
4. `git rm phase2/docker/docker-compose_auth.yml-notused`
5. `git rm phase2/python_PoC_scripts/rag_weaviate_pdf_PoC.py` (exact duplicate of `rag_weaviate_pdf.py`)

**Files to delete**: 5 files listed above.

### Task 1.5: Deduplicate windows_ip_in_wsl.py

**Why**: 3 tracked Python copies exist. Keep one canonical copy.

**Steps**:
1. Keep `phase1/python_code/windows_ip_in_wsl.py` as canonical
2. `git rm phase2/RAG_app/windows_ip_in_wsl.py` (identical to phase1)
3. `git rm phase2/python_PoC_scripts/windows_ip_in_wsl.py` (PoC variant)
4. Check for imports in `phase2/RAG_app/` files: `config.py`, `qa_loop.py`, `retriever.py`, `ingest_pdf.py`

**Files to delete**: 2 copies
**Files to keep**: `phase1/python_code/windows_ip_in_wsl.py`, `phase1/batch_and_shell/windows_ip_in_wsl.sh`

### Task 1.6: Clean Commented-Out Code in helper_functions.py

**Why**: `phase1/python_code/helper_functions.py` is 177 lines, ~120 are commented-out dead code. Active code is only `get_llm_response` at lines 140-176.

**Steps**:
1. Keep module docstring, active imports (lines 2-3), and `get_llm_response` function (lines 140-176)
2. Remove everything between lines 8-138
3. Result: ~45 lines

**Files to modify**: `phase1/python_code/helper_functions.py`

---

## Phase 2: Unify Configuration (Sequential — 2.1 first, then 2.2/2.3 parallel, then 2.4)

### Task 2.1: Standardize Python 3.12 and Remove Legacy setup.cfg

**Why**: 4 different Python versions referenced: pyproject.toml (>=3.12), setup.cfg (>=3.11), CI (3.11), devcontainer (3.13).

**Steps**:
1. Edit `.github/workflows/python-lint-test.yml`: change `python-version: '3.11'` → `'3.12'`
2. Delete `phase0/setup.cfg` entirely (legacy setuptools config; console_scripts entry point references non-existent path)
3. Add `[tool.pytest.ini_options]` to `pyproject.toml`:
   ```toml
   [tool.pytest.ini_options]
   addopts = "-ra -q"
   testpaths = ["phase0/tests", "phase1/tests", "phase2/tests"]
   ```

**Files to modify**: `.github/workflows/python-lint-test.yml`, `pyproject.toml`
**Files to delete**: `phase0/setup.cfg`

### Task 2.2: Replace flake8 + black with ruff

**Why**: Ruff replaces flake8, black, isort in a single tool, 10-100x faster. Natural companion to uv (already in devcontainer).

**Steps**:
1. Replace `[tool.black]` in `pyproject.toml` with:
   ```toml
   [tool.ruff]
   line-length = 120
   target-version = "py312"

   [tool.ruff.lint]
   select = ["E", "F", "W", "I"]
   ignore = ["E203", "E401", "E302", "E305"]

   [tool.ruff.format]
   quote-style = "double"
   ```
2. Delete `.flake8`
3. Update `.pre-commit-config.yaml`:
   ```yaml
   repos:
     - repo: https://github.com/astral-sh/ruff-pre-commit
       rev: v0.11.6
       hooks:
         - id: ruff
           args: [--fix]
         - id: ruff-format
   ```
4. Update `.vscode/settings.json`: replace black-formatter with `charliermarsh.ruff`, remove cornflakes/flake8 lines
5. Update `hands-on-llm.code-workspace`: replace `ms-python.black-formatter` with `charliermarsh.ruff`
6. Update `.vscode/extensions.json`: add `charliermarsh.ruff`
7. Run `ruff format .` and `ruff check --fix .` to reformat codebase

**Files to modify**: `pyproject.toml`, `.pre-commit-config.yaml`, `.vscode/settings.json`, `hands-on-llm.code-workspace`, `.vscode/extensions.json`
**Files to delete**: `.flake8`

### Task 2.3: Consolidate Dependencies into pyproject.toml

**Why**: 3 separate `requirements.txt` with heavy overlap + root `pyproject.toml` with minimal deps. No lock files.

**Steps**:
1. Restructure `pyproject.toml` with `[project.optional-dependencies]`:
   - `phase0`, `phase1`, `phase2` extras for phase-specific deps
   - `dev` extra for ruff, pytest, mypy, pre-commit
2. Add `[tool.uv.sources]` for torch CUDA index:
   ```toml
   [tool.uv.sources]
   torch = { index = "pytorch-cu128" }

   [[tool.uv.index]]
   name = "pytorch-cu128"
   url = "https://download.pytorch.org/whl/cu128"
   ```
3. Run `uv lock` to generate `uv.lock`
4. Add deprecation header to each `requirements.txt`:
   ```
   # DEPRECATED: Dependencies now managed in root pyproject.toml.
   # Install with: uv sync --extra phase2 --extra dev
   # This file kept as documentation only.
   ```

**Files to modify**: `pyproject.toml`, `phase0/requirements.txt`, `phase1/requirements.txt`, `phase2/requirements.txt`
**Files to create**: `uv.lock` (generated)

### Task 2.4: Rewrite CI Workflow

**Why**: Current CI only runs `black .`. After ruff migration, CI should use ruff + uv + pytest.

**Steps**:
1. Rewrite `.github/workflows/python-lint-test.yml`:
   ```yaml
   name: Lint and Test

   on:
     push:
       branches: [main]
     pull_request:
       branches: [main]

   jobs:
     lint:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - uses: astral-sh/setup-uv@v6
         - uses: astral-sh/ruff-action@v3
           with:
             args: "check"
         - uses: astral-sh/ruff-action@v3
           with:
             args: "format --check"

     test:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - uses: astral-sh/setup-uv@v6
         - run: uv sync --extra dev
         - run: uv run pytest --tb=short || true
   ```
   Note: `|| true` on pytest because tests require GPU/Ollama. Remove when tests are mockable.

**Files to modify**: `.github/workflows/python-lint-test.yml`

---

## Phase 3: Code Quality (All Tasks Independent)

### Task 3.1: Expand Pre-Commit Hooks

**Steps**:
1. Add to `.pre-commit-config.yaml`:
   ```yaml
   repos:
     - repo: https://github.com/pre-commit/pre-commit-hooks
       rev: v5.0.0
       hooks:
         - id: trailing-whitespace
         - id: end-of-file-fixer
         - id: check-yaml
         - id: check-added-large-files
           args: ['--maxkb=500']
     - repo: https://github.com/astral-sh/ruff-pre-commit
       rev: v0.11.6
       hooks:
         - id: ruff
           args: [--fix]
         - id: ruff-format
   ```

**Files to modify**: `.pre-commit-config.yaml`

### Task 3.2: Add __init__.py to Python Directories

**Why**: Directories lack `__init__.py`, making imports fragile.

**Files to create** (empty):
- `phase0/python_scripts/__init__.py`
- `phase0/tests/__init__.py`
- `phase1/python_code/__init__.py`
- `phase1/tests/__init__.py`
- `phase2/RAG_app/__init__.py`
- `phase2/python_PoC_scripts/__init__.py`
- `phase2/tests/__init__.py`

### Task 3.3: Add Minimal phase2 Smoke Test

**Why**: `phase2/tests/` is empty.

**Steps**:
1. Create `phase2/tests/test_config.py`:
   ```python
   """Smoke test: verify phase2 RAG_app modules are importable."""

   def test_config_constants():
       from phase2.RAG_app.config import COLLECTION_NAME, CHUNK_SIZE
       assert isinstance(COLLECTION_NAME, str)
       assert CHUNK_SIZE > 0
   ```

**Files to create**: `phase2/tests/test_config.py`

### Task 3.4: Add pytest Config to pyproject.toml

**Why**: pytest config currently in `phase0/setup.cfg` which will be deleted in Task 2.1.

**Steps**: Covered in Task 2.1 — add `[tool.pytest.ini_options]` to `pyproject.toml`.

---

## Phase 4: Polish (Nice-to-Have, Low Risk, All Independent)

### Task 4.1: Clean Up .vscode/extensions.json

Replace with ruff + python recommendations only.

**Files to modify**: `.vscode/extensions.json`

### Task 4.2: Fix phase0/Makefile Python Pinning

Change `PYTHON_EXECUTABLE ?= python3.11` → `python3` on line 5.

**Files to modify**: `phase0/Makefile`

### Task 4.3: Add `from __future__ import annotations` to All ~28 Own-Code .py Files

**Why**: Consistent forward-compatible type hint syntax across Python 3.12/3.13.

**Scope**: All `.py` files in phase0/phase1/phase2 except `AI-Python-for-Beginners_local_LLM/` course materials.

---

## What Stays Untouched

- **3-phase directory structure** — intentional, preserved
- **Devcontainer setup** — already modern (uv, Python 3.13, zsh)
- **AI-Python-for-Beginners_local_LLM/** — third-party course materials
- **Jupyter notebooks** — learning artifacts
- **phase1/batch_and_shell/windows_ip_in_wsl.sh** — separate bash artifact

## Audit Corrections

- `.env` files and `phase2/data/` (105MB) are **not** committed to git (`.gitignore` catches them)
- Real risk is accidental `git add -f` or `.gitignore` edits — hence defense-in-depth patterns
