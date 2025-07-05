from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage, HumanMessage

"""
Helper functions for LLM and benchmarking scripts.
"""

# this helper_functions was modified to use local Ollama server instead of OpenAI's cloud API.

"""
# Get the OpenAI API key from the .env file
load_dotenv('.env', override=True)
openai_api_key = os.getenv('OPENAI_API_KEY')

# Set up the OpenAI client
client = OpenAI(api_key=openai_api_key)
"""

'''
# import gradio as gr
from dotenv import load_dotenv
import csv

def print_llm_response(prompt):
    """This function takes as input a prompt, which must be a string enclosed in quotation marks,
    and passes it to OpenAI's GPT3.5 model. The function then prints the response of the model.
    """
    try:
        if not isinstance(prompt, str):
            raise ValueError("Input must be a string enclosed in quotes.")
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful but terse AI assistant who gets straight to the point."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.0,
        )
        response = completion.choices[0].message.content
        print(response)
    except TypeError as e:
        print("Error:", str(e))
'''

''' This OpenAI function is replaced by local Ollama function VER 3 below.
def get_llm_response(prompt):
    """This function takes as input a prompt, which must be a string enclosed in quotation marks,
    and passes it to OpenAI's GPT3.5 model. The function then saves the response of the model as
    a string.
    """
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful but terse AI assistant who gets straight to the point."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.0,
    )
    response = completion.choices[0].message.content
    return response
'''

'''This function is replaced by VER 3 function below.'
from langchain_ollama import OllamaLLM
def get_llm_response(prompt):
    # VER 1 of local Ollama function: NB!!! it requires token loop because of streaming
    llm = OllamaLLM(model="mistral", base_url="http://localhost:11434")
    response = llm.invoke(prompt)
    return response.strip()
    """
    Example usage
    myprompt = "Write the summary of the book 'The Alchemist', by Paulo Coelho"
    for text in llm.invoke(myprompt):
        print(text, end="", flush=True)
    """
'''

'''
# This function is replaced by VER 3 function below.
# Set up the OpenAI client to hit Ollama instead of the cloud
client = OpenAI(
    api_key='ollama',
    # Ollama does not require an API key, so we use a placeholder
    # If you set it to None, you will get an error.
    base_url="http://localhost:11434/v1" # Ollama’s OpenAI-compatible endpoint
)

def get_llm_response(prompt):
    """
    TESTED, WORKED in my local jupyter notebook!
    VER 2 of local Ollama function: it uses local Ollama server via OpenAI API client.
    """
    completion = client.chat.completions.create(
        model="mistral",       # ← pick any model you’ve `ollama pull`-ed
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful but terse AI assistant who gets straight to the point."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.0,
        stream=False,          # to stream you pass stream=True in the payload;
        # if you omit the field (or set False) you stay in non-streaming mode.
    )
    #  if streaming is enabled, uncomment the following lines to handle the response
    """
    response = ""
    for delta in completion:
        response += delta.choices[0].delta.content
    """
    #  if stream is returned by the function, use the following lines in calling code
    """
    for delta in stream:
        print(delta.choices[0].delta.content, end="", flush=True)
    """
    response = completion.choices[0].message.content
    return response + "\n VER 2 WORKS!"
'''

# This function is replacing the OpenAI get_llm_response function above.
# It uses the ChatOllama class from the langchain_ollama package to interact with a local Ollama
# server.
# The endpoint is the OpenAI-compatible /v1/chat/completions API.


def get_llm_response(
    prompt: str,
    *,
    model: str = "mistral",
    base_url: str = "http://localhost:11434",
    system_prompt: str = (
        "You are a helpful but terse AI assistant who gets straight to the point."
    ),
    temperature: float = 0.0,
    num_predict: int = 100,  # Reduced default value
    stream: bool = False,
    num_ctx: int = 8192,  # context size
) -> str:  # Send `prompt` to a local Ollama model and return the full reply text.
    """
    TESTED, WORKED in my local jupyter notebook!
    VER 3 of local Ollama function: it uses local Ollama server via OpenAI API client.
    This function is replacing the OpenAI get_llm_response function above.
    It uses the OllamaLLM class from the langchain_ollama package to interact with a local Ollama
    server.
    Send `prompt` to a local Ollama model and return the full reply text.
    If stream=True, the raw response is returned as a string that you can parse into JSON.
    If stream=False, the text content of the response is returned as a string.

    Note: the stream=True case returns a raw JSON string, not a parsed object.
    """
    llm = ChatOllama(
        model=model,
        base_url=base_url,
        system=system_prompt,
        temperature=temperature,
        num_predict=num_predict,
        num_ctx=num_ctx,
        streaming=stream,
    )
    # If streaming, return the raw response so the caller can parse the JSON.
    if stream:
        return llm.invoke(prompt)
    else:
        return llm.generate([[HumanMessage(content=prompt)]]).generations[0][0].text.strip()
