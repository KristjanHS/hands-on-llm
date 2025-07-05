#!/bin/bash
# This script sends a POST request to the Ollama API with a JSON payload.

# Get the directory where this script is located to reliably find the helper script.
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)

# Dynamically detect WIN_IP using the helper script.
WIN_IP_SCRIPT="$SCRIPT_DIR/windows_ip_in_wsl.sh"

# Check for the helper script first.
if [[ ! -f "$WIN_IP_SCRIPT" ]]; then
    echo "Error: IP helper script not found at '$WIN_IP_SCRIPT'" >&2
    exit 1
fi

# Execute the helper script and capture the IP.
# The helper script outputs the IP to stdout on success.
WIN_IP=$("$WIN_IP_SCRIPT")

# Exit if the helper script failed (it prints its own error message to stderr).
if [[ -z "$WIN_IP" ]]; then
    echo "Error: Could not determine Windows host IP." >&2
    exit 1
fi

# Note: Ensure that `payload.json` exists in the directory where you run this script.
curl -v \
   -H "Content-Type: application/json" \
   -d @payload.json \
   "http://$WIN_IP:11434/v1/chat/completions"
