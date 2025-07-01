import requests

host = "http://localhost:11434" # WSL ollama host
#host = "http://172.22.208.1:11434" # windows ollama host

response = requests.get(f"{host}/api/tags")
print(response.json())
