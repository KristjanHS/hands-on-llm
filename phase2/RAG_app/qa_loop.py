#!/usr/bin/env python3
"""Interactive console for Retrieval-Augmented Generation."""
from __future__ import annotations

import sys

try:
    from langchain_ollama import ChatOllama
except ImportError:  # Graceful fallback if package missing
    ChatOllama = None  # type: ignore

from config import OLLAMA_MODEL, OLLAMA_URL
from retriever import get_top_k


def build_prompt(question: str, context_chunks: list[str]) -> str:
    context = "\n\n".join(context_chunks)
    prompt = (
        "You are a helpful assistant who answers strictly from the provided context.\n\n"
        f'Context:\n"""\n{context}\n"""\n\n'
        f"Question: {question}\nAnswer:"
    )
    return prompt


def answer(question: str, k: int = 5) -> str:
    chunks = get_top_k(question, k=k)
    if not chunks:
        return "I found no relevant context to answer that question."

    if ChatOllama is None:
        return "[langchain_ollama not installed]"

    llm = ChatOllama(model=OLLAMA_MODEL, base_url=OLLAMA_URL)
    return str(llm.invoke(build_prompt(question, chunks)))


if __name__ == "__main__":
    print("RAG console – type a question, Ctrl-D/Ctrl-C to quit")
    try:
        for line in sys.stdin:
            q = line.strip()
            if not q:
                continue
            print("→", answer(q), "\n")
    except (EOFError, KeyboardInterrupt):
        pass
