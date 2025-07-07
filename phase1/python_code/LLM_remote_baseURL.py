#!/usr/bin/env python3
# Text-completion style (LLM interface) ------------
from langchain_ollama import OllamaLLM

llm = OllamaLLM(
    model="llama3:instruct",  # tag that exists locally
    base_url="https://nearby-adequately-python.ngrok-free.app",
    temperature=0.0,
)

print(llm.invoke("Say hello in Estonian"))

"""
IT WORKED against the remote Ollama server!
The response is:
(.venv) kristjans@DESKTOP-26A9125:~/projects/hands-on-llm/phase1$
 /home/kristjans/projects/hands-on-llm/.venv/bin/python
 /home/kristjans/projects/hands-on-llm/phase1/src/L2-LLM_remote_baseURL.py
In Estonian, you can say "Tere!" (pronounced "teh-reh")
to say hello. This is a casual way of greeting someone.

If you want to be more formal, you can say "Hei!" (pronounced "hay"),
which is similar to saying "hello" in English.

There are also other ways to greet someone in Estonian, depending on the time of day:

* "Tere hommikust!" (pronounced "teh-reh hoh-mee-koo-st") means "good morning!"
* "Tere päeva!" (pronounced "teh-reh pyeh-vah") means "good afternoon!"
* "Tere õhtust!" (pronounced "teh-reh ooh-hoost") means "good evening!"
"""
