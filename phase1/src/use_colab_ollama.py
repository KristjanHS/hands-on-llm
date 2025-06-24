from ollama import Client  
  
#Replace the URL with your localtunnel URL  
host = 'https://hip-waves-doubt.loca.lt/'  
  
# Initialize the Ollama client.  
ollama_client = Client(host)  
  
# Prepare the message to send to the LLaVA model.  
message = {  
    'role': 'user',  
    'content': 'What is in this picture?',  
    'images': ['/9j/4AAQSkZJRgABAQEAYABgAAD/4QAiRXhpZgAATU0AKgAAAAgAAQESAAMAAAABAAEAAAAAAAD/2wBDAAIBAQIBAQICAgICAgICAwUDAwMDAwYEBAMFBwYHBwcGBwcICQsJCAgKCAcHCg0KCgsMDAwMBwkODw0MDgsMDAz/2wBDAQICAgMDAwYDAwYMCAcIDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAz/wAARCAAcAAoDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwDv7jwn5OqWEeGXzjKMAcHameav/wDCE/7H6V1/jFNL0L4l+EdNuri3hvL95/Jjd9pbcmwfm3Az1Ndv/wAIUB/yz/Sv3fD5nF1KqT2kv/SYn5DiMLNU6Urbxf8A6UzzH4meLm8WfEfVrjTdGbVLrw+IbfTLyEyMllLBL50zPhP4vukDOFGe9ezaH8XvDWuaLZ3v9q2cf2yBJ9gbhNyhsc4PGe4Br6F+Gf8AwSY+GvwVso7DwzrHj/TbCzkuLuO3/tvzVE84CyybnQsCyqF2hgmP4c81yFx/wQh+BN3cSSt/wnStIxchfEMiqCeeABgD2r8Kp8QYynOU4297f8+3mfqVfK8JUhCDjsv6/LyP/9k=']  
}  
  
# Use the ollama.chat function to send the image and retrieve the description.  
try:  
    response = ollama_client.chat(  
        model = "llava:13b",  # Specify LLaVA model size and version hosted  
        messages = [message]  
        )  
except ollama_client.ResponseError as e:  
    print('Error:', e.error)  
  
# Print the model's description of the image  
response = response['message']['content']  
print(response)