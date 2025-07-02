# This script sends a POST request to the Ollama API with a JSON payload.
# Dynamically detect WIN_IP using windows_ip_in_wsl.sh before running:
WIN_IP=$(bash windows_ip_in_wsl.sh) 
export WIN_IP
# Note: Ensure that the `windows_ip_in_wsl.sh` script is executable and in your PATH.

curl -v \
   -H "Content-Type: application/json" \
   -d @payload.json \
   http://$WIN_IP:11434/v1/chat/completions
