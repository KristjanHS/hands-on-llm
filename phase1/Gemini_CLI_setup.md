# Gemini CLI chat — WSL 2 Setup Guide (Phase 1 Companion)

This document distills the raw shell history from *phase 1* into a **clean, replay‑able reference** for installing and using Google’s **Gemini CLI chat** inside Ubuntu on WSL 2.  The structure mirrors the style of the existing `README.md` files for Phase 0 and Phase 1 so you can drop it straight into the repo.

> **Why Gemini CLI chat?**  
* It puts Gemini 2.5 Pro (and newer) models directly in your terminal, supports ReAct loops with your local tools, and integrates with VS Code & shell scripts — all without leaving WSL 2. 
* CLI offers a higher FREE daily quota (up to 1,000 requests) compared to Gemini Code Assist, while still able to run the changes across the project the AGENTIC way.

**If you want to ensure the Agentic CLI always uses Gemini Pro and does not fall back to Gemini Flash:
* Switch to "Direct API Mode" in Agentic CLI (after /auth): provide Gemini API Key to CLI through your project .env file.

---

## Important - Understand the difference: Gemini Code Assist (IDE) vs. Gemini CLI (Agentic Mode)

Gemini CLI's Agentic Mode cannot replicate the safe, complex, multi-file refactoring of the IDE's Gemini Code Assist. They operate on fundamentally different principles.

### The Analogy: The Resident Surgeon vs. The Remote-Controlled Robot

*   **Gemini Code Assist (IDE) is the Resident Surgeon:** It lives inside the operating room (the IDE). It has a deep, semantic understanding of the patient's anatomy (your code's structure via AST). When it makes a change, it uses precise, specialized surgical tools (the IDE's safe refactoring engine).

*   **Gemini CLI Agent is the Remote-Controlled Robot:** It operates from outside the room, looking in through a camera (the shell). It explores by running commands (`ls`, `cat`). When it makes a change, it uses powerful but general-purpose tools from its toolkit (`sed`, `awk`, file overwrites), which are riskier and lack surgical precision.

### Key Differences at a Glance

| Feature | Gemini Code Assist (IDE) | Gemini CLI (Agentic Mode) |
| :--- | :--- | :--- |
| **Project Context** | **Deep & Semantic** (understands code structure) | **Shallow & Exploratory** (runs shell commands like `ls`, `cat`) |
| **Code Modification** | **Safe & Structured** (uses the IDE's refactoring engine) | **Text-Based & Risky** (uses tools like `sed` or file overwrites) |
| **Primary Strength** | Complex, context-aware code generation and refactoring | Automation, scripting, and executing shell workflows |
| **Best For** | "Rename this function and all its usages across 10 files." | "Find all files using the 'requests' library and list them." |

### When to Use Which

**Use Gemini Code Assist (IDE) for:**
-   Safely refactoring code across your entire project.
-   Generating complex functions or classes that are aware of existing code.
-   Understanding and explaining large, intricate codebases.

**Use the Gemini CLI Agent for:**
-   Automating shell tasks (e.g., "Find all TODOs in `.py` files and save them to a list").
-   Querying your project ("Which files import the `os` module?").
-   Generating boilerplate, scripts, or configuration files.

### The Bottom Line

They are complementary tools, not interchangeable. The IDE is for **developing and understanding** code; the CLI agent is for **operating on and automating** your development environment.

---

## 0  Prerequisites

```bash
# WSL 2 Ubuntu 22.04 (or 20.04) already running
# Phase 0 & Phase 1 prerequisites satisfied (GPU, CUDA, Python, etc.)

# Google Cloud account with Gemini Code Assist enabled
# A GCP project + billing (free individual tier works)
```

You **don’t** need a GPU for Gemini CLI itself, but if you plan on local model work you’ll want the Phase 1 CUDA stack.

---

## 1  Quick‑start (copy‑paste)

```bash
# 1  Install Node 20 LTS via NodeSource
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs   # brings along npm 10+

# 2  Install Gemini CLI globally (preferred)
sudo npm install -g @google/gemini-cli

# 3  Log in to Google Cloud and set project / region
gcloud auth login                # opens browser
PROJECT_ID="my‑gemini‑lab"
gcloud config set project $PROJECT_ID
gcloud services enable aiplatform.googleapis.com
gcloud config set ai/region europe-north1  # pick a supported region

# 4  Run the CLI
gemini --version                 # sanity check
gemini chat -m gemini-1.5-pro-preview
```

> **Ad‑hoc usage:** `npx @google/gemini-cli` works without a global install.

---

## 2  Install Node 20 LTS (detailed)

1. **Add the NodeSource repository**

   ```bash
   curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
   ```
2. **Install Node & npm**

   ```bash
   sudo apt-get install -y nodejs
   node -v   # v20.x
   npm -v    # 10.x+
   ```
3. *(Optional)* update npm separately:

   ```bash
   sudo npm install -g npm@latest
   ```

---

## 3  Install Gemini CLI

### 3.1 Global install

```bash
sudo npm install -g @google/gemini-cli
```

### 3.2 One‑shot via npx

```bash
npx @google/gemini-cli  # runs the latest published version
```

The first run may download additional packages and create `~/.gemini/` for config.

---

## 4  Configure Google Cloud authentication

Gemini CLI piggybacks on the **gcloud SDK**.  If you skipped Phase 0/1 cloud steps:

```bash
# Install Google Cloud CLI (official Debian/Ubuntu repo)
sudo apt-get update && sudo apt-get install -y ca-certificates gnupg
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://packages.cloud.google.com/apt/doc/apt-key.gpg | \
  sudo gpg --dearmor -o /etc/apt/keyrings/cloud.google.gpg

echo "deb [signed-by=/etc/apt/keyrings/cloud.google.gpg] \
  https://packages.cloud.google.com/apt cloud-sdk main" | \
  sudo tee /etc/apt/sources.list.d/google-cloud-sdk.list

sudo apt-get update && sudo apt-get install -y google-cloud-cli
```

Then authenticate and choose a project:

```bash
# Browser login (creates ADC credentials)
gcloud auth login

# Pick or create a project
gcloud projects create my‑gemini‑lab --set-as-default  # if new

# Enable Vertex AI
gcloud services enable aiplatform.googleapis.com

# Set default region (Gemini supports europe‑north1, us‑central1, …)
gcloud config set ai/region europe-north1
```

---

## 5  First commands

```bash
# Check models you can access
gemini models list

# Chat REPL with the default model
gemini chat -m gemini-1.5-pro-preview

# One‑liner completion
echo "Write a haiku about WSL" | gemini prompt -m gemini-1.5-pro-preview
```

Gemini CLI supports **ReAct loops**: give it goals like *“add unit tests for my project”* and it will plan actions, run shell commands, edit files and ask for confirmation.

---

## 6  Upgrading & Uninstalling

```bash
# Upgrade to the latest npm release
sudo npm update -g @google/gemini-cli

# Remove it entirely
sudo npm uninstall -g @google/gemini-cli
```

---

## 7  Troubleshooting

| Symptom                              | Fix                                                                                     |
| ------------------------------------ | --------------------------------------------------------------------------------------- |
| `gemini: command not found`          | Ensure `npm bin -g` (usually `/usr/local/bin`) is on `$PATH`.                           |
| `Error: no ADC credentials`          | Run `gcloud auth login` again or `gcloud auth application-default login`.               |
| `PERMISSION_DENIED` when calling API | Verify billing is enabled **and** `aiplatform.googleapis.com` is active on the project. |
| CLI hangs inside VS Code             | Try `wsl.exe --shutdown`, then relaunch VS Code Remote or run from a plain WSL shell.   |

---

## 8  Reference links

* Official docs: [https://cloud.google.com/gemini/docs/codeassist/gemini-cli](https://cloud.google.com/gemini/docs/codeassist/gemini-cli)
* GitHub repo: [https://github.com/google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli)
* Announcement blog: [https://cloud.google.com/blog/products/ai-machine-learning/introducing-gemini-cli](https://cloud.google.com/blog/products/ai-machine-learning/introducing-gemini-cli)

---

### End of Gemini CLI Guide

You now have a reproducible, **one‑file** recipe to bring Gemini to your WSL 2 terminal.  Happy hacking!
