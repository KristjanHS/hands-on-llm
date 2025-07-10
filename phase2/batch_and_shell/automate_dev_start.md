# Automating Project Startup with Virtual Environment Activation and VS Code

This guide describes how to automate the following steps in your WSL shell:

```bash
cd projects/hands-on-llm/
source .venv/bin/activate
code .
```

So that the shell ends up in:

```bash
((.venv) ) username@PCname:~/projects/hands-on-llm$
```

---

## Step 1: Create the Shell Script

Save the following script as `start_llm.sh` in your home directory:

```bash
#!/bin/bash

# Navigate to the project directory
cd ~/projects/hands-on-llm || {
  echo "Project directory not found."
  return 1
}

# Activate the virtual environment
if [ -f .venv/bin/activate ]; then
  source .venv/bin/activate
else
  echo "Virtual environment not found."
  return 1
fi

# Open VS Code in the current directory
code .
```

---

## Step 2: Make the Script Executable

```bash
chmod +x ~/start_llm.sh
```

---

## Step 3: Source the Script

To ensure the environment persists in the current shell session, source the script:

```bash
source ~/start_llm.sh
```

### Optional: Add an Alias

Add this to your `.bashrc` or `.zshrc`:

```bash
alias llm='source ~/start_llm.sh'
```

Reload your shell config:

```bash
source ~/.bashrc  # or source ~/.zshrc
```

Now, run `llm` anytime to initialize your project.

---

## Why Source Instead of Execute?

Running a script normally (`./start_llm.sh`) launches a subshell, so environment changes like `source .venv/bin/activate` won't persist.

By **sourcing**, the commands run in the **current** shell, so the virtual environment remains active.

See: [StackOverflow explanation](https://stackoverflow.com/questions/13122137/how-to-source-virtualenv-activate-in-a-bash-script)

---

## Optional: Auto-Activate on `cd`

To automatically activate the environment when entering the directory, add this to `.bashrc` or `.zshrc`:

```bash
function cd() {
  builtin cd "$@" || return
  if [ -f .venv/bin/activate ]; then
    source .venv/bin/activate
  fi
}
```

**Caution:** Overriding `cd` can have side effects. Only use if it fits your workflow.

Ref: [Ask Ubuntu suggestion](https://askubuntu.com/questions/791351/run-virtualenv-in-new-terminal-tab-automatically)
