#!/usr/bin/env python3
"""
I FINALLY GOT this code to work against the Ollama Colab server, which is running the LLaVA model.
The Colab also uses Ngrok to tunnel the local Ollama server to the internet, so that it can be accessed from My local VScode.
On Colab, make sure to run the Ollama server first, and then start Ngrok to tunnel the server.
The LLaVA model is a large language and vision model that can describe images in natural language.
The code sends an image to the LLaVA model and retrieves a description of the image.
"""
from ollama import Client

# Replace the URL with your localtunnel URL
host = "https://nearby-adequately-python.ngrok-free.app/"

# Initialize the Ollama client.
ollama_client = Client(host)

# Prepare the message to send to the LLaVA model.
message = {
    "role": "user",
    "content": "What is in this picture?",
    "images": [
        "/9j/4AAQSkZJRgABAQEAYABgAAD/4QAiRXhpZgAATU0AKgAAAAgAAQESAAMAAAABAAEAAAAAAAD/2wBDAAIBAQIBAQICAgICAgICAwUDAwMDAwYEBAMFBwYHBwcGBwcICQsJCAgKCAcHCg0KCgsMDAwMBwkODw0MDgsMDAz/2wBDAQICAgMDAwYDAwYMCAcIDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAz/wAARCAAcAAoDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwDv7jwn5OqWEeGXzjKMAcHameav/wDCE/7H6V1/jFNL0L4l+EdNuri3hvL95/Jjd9pbcmwfm3Az1Ndv/wAIUB/yz/Sv3fD5nF1KqT2kv/SYn5DiMLNU6Urbxf8A6UzzH4meLm8WfEfVrjTdGbVLrw+IbfTLyEyMllLBL50zPhP4vukDOFGe9ezaH8XvDWuaLZ3v9q2cf2yBJ9gbhNyhsc4PGe4Br6F+Gf8AwSY+GvwVso7DwzrHj/TbCzkuLuO3/tvzVE84CyybnQsCyqF2hgmP4c81yFx/wQh+BN3cSSt/wnStIxchfEMiqCeeABgD2r8Kp8QYynOU4297f8+3mfqVfK8JUhCDjsv6/LyP/9k="
    ],
}

# Use the ollama.chat function to send the image and retrieve the description.
try:
    response = ollama_client.chat(model="llava:13b", messages=[message])  # Specify LLaVA model size and version hosted
except ollama_client.ResponseError as e:
    print("Error:", e.error)

# Print the model's description of the image
response = response["message"]["content"]
print(response)

"""
(.venv) kristjans@DESKTOP-26A9125:~/projects/hands-on-llm/phase1$ 
/home/kristjans/projects/hands-on-llm/.venv/bin/python /home/kristjans/projects/hands-on-llm/phase1/src/use_colab_ollama.py
 The image shows a very blurred Eiffel Tower, which is an iconic landmark located in Paris, France. 
 The tower appears to be slightly tilted and the sky is blue, suggesting it might be taken during the day under bright sunlight. 
 Due to the lack of clarity, it's difficult to provide more details about the scene or the context.
"""
