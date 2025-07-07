#!/usr/bin/env python3
import requests
from phase1.python_code.windows_ip_in_wsl import get_windows_host_ip

# Uses get_windows_host_ip from windows_ip_in_wsl.py
host_ip = get_windows_host_ip() or "localhost"
host = f"http://{host_ip}:11434"

response = requests.get(f"{host}/api/tags")
print(response.json())
