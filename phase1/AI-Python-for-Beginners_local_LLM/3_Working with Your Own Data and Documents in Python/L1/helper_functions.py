# this helper_functions was modified to use local Ollama server instead of OpenAI's cloud API.

# import gradio as gr
import os
from openai import OpenAI
from dotenv import load_dotenv
import csv

from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage


# Get the OpenAI API key from the .env file
load_dotenv(".env", override=True)
openai_api_key = os.getenv("OPENAI_API_KEY")

# Set up the OpenAI client
client = OpenAI(api_key=openai_api_key)


def read_csv_dict(csv_file_path):
    """This function takes a csv file and loads it as a dict."""

    # Initialize an empty list to store the data
    data_list = []

    # Open the CSV file
    with open(csv_file_path, mode="r") as file:
        # Create a CSV reader object
        csv_reader = csv.DictReader(file)

        # Iterate over each row in the CSV file
        for row in csv_reader:
            # Append the row to the data list
            data_list.append(row)

    # Convert the list to a dictionary
    data_dict = {i: data_list[i] for i in range(len(data_list))}
    return data_dict


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
                    "content": "You are a helpful but terse AI assistant who gets straight to the point.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.0,
        )
        response = completion.choices[0].message.content
        print(response)
    except TypeError as e:
        print("Error:", str(e))


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
                "content": "You are a helpful but terse AI assistant who gets straight to the point.",
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
    """
    # VER 1 of local Ollama function: NB!!! it requires token loop because of streaming
    """
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
                "content": "You are a helpful but terse AI assistant who gets straight to the point.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.0,
        stream=False,
        # to stream you pass stream=True in the payload;
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


def get_llm_response(
    prompt: str,
    *,
    model: str = "mistral",
    base_url: str = "http://localhost:11434",
    system_prompt: str = (
        "You are a helpful but terse AI assistant who gets straight to the point."
    ),
    temperature: float = 0.0,
) -> str:  # Send `prompt` to a local Ollama model and return the full reply text.
    """
    TESTED, WORKED in my local jupyter notebook!
    VER 3 of local Ollama function: it uses local Ollama server via OpenAI API client.
    This function is replacing the OpenAI get_llm_response function above.
    It uses the OllamaLLM class from the langchain_ollama package to interact with a local Ollama server.
    """
    llm = ChatOllama(
        model=model,
        base_url=base_url,
        system=system_prompt,
        temperature=temperature,
        streaming=False,  # one-shot response, no token loop
    )
    message: AIMessage = llm.invoke(prompt)  # returns a ChatMessage
    return (
        message.content.strip() + "\n VER 3 WORKS!"
    )  # Return the response text, ensuring it ends with a newline for consistency.


def get_chat_completion(prompt, history):
    history_string = "\n\n".join(["\n".join(turn) for turn in history])
    prompt_with_history = f"{history_string}\n\n{prompt}"
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful but terse AI assistant who gets straight to the point.",
            },
            {"role": "user", "content": prompt_with_history},
        ],
        temperature=0.0,
    )
    response = completion.choices[0].message.content
    return response
