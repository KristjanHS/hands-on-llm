# Gemini CLI — WSL 2 Setup Guide (Phase 1 Companion)

This document distills the raw shell history from *phase 1* into a **clean, replay‑able reference** for installing and using Google’s **Gemini CLI** inside Ubuntu on WSL 2.  The structure mirrors the style of the existing `README.md` files for Phase 0 and Phase 1 so you can drop it straight into the repo.

> **Why Gemini CLI?**  It puts Gemini 2.5 Pro (and newer) models directly in your terminal, supports ReAct loops with your local tools, and integrates with VS Code & shell scripts — all without leaving WSL 2. CLI offers a higher FREE daily quota (up to 1,000 requests) compared to Gemini Code Assist, while still doing the changes across the project the agentic way.

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
