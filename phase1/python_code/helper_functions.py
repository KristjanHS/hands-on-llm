#!/usr/bin/env python3
"""
Helper functions for LLM and benchmarking scripts.
"""

from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage


def get_llm_response(
    prompt: str,
    *,
    model: str = "mistral",
    base_url: str = "http://localhost:11434",
    system_prompt: str = ("You are a helpful but terse AI assistant who gets straight to the point."),
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
