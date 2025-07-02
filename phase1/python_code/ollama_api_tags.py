import requests
from phase1.python_code.windows_ip_in_wsl import get_windows_host_ip

host = f"http://{get_windows_host_ip() or 'localhost'}:11434" # Uses get_windows_host_ip from windows_ip_in_wsl.py

response = requests.get(f"{host}/api/tags")
print(response.json())
