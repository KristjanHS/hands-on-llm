#!/usr/bin/env python3
# This script benchmarks the Ollama API by sending a chat completion request
# and measuring the response time, while also collecting token usage statistics.
# It uses the get_llm_response function from helper_functions.py to interact with a
# local Ollama server.
# The endpoint is the OpenAI-compatible /v1/chat/completions API.

import argparse
import time
import statistics

# from typing import Optional

from helper_functions import get_llm_response
from phase1.python_code.windows_ip_in_wsl import get_windows_host_ip


def parse_args():
    p = argparse.ArgumentParser(
        description="Benchmark local Ollama inference using get_llm_response"
    )
    p.add_argument(
        "--prompt", "-p", default="Hello, how are you?", help="Text prompt to send"
    )
    p.add_argument(
        "--model",
        "-m",
        default="mistral",
        help="Ollama model name (default: mistral)",
    )
    p.add_argument(
        "--base-url",
        "-b",
        default=(f"http://{get_windows_host_ip() or 'localhost'}:11434"),
        help=(
            "Base URL for local Ollama server "
            "(default: detected Windows host IP, or localhost if not found)"
        ),
        # Uses get_windows_host_ip from windows_ip_in_wsl.py
    )
    p.add_argument(
        "--temperature",
        "-t",
        type=float,
        default=0.0,
        help="Sampling temperature (default: 0.0)",
    )
    p.add_argument(
        "--runs", "-r", type=int, default=5, help="Number of timed runs (default: 5)"
    )
    return p.parse_args()


def benchmark(prompt: str, model: str, base_url: str, temperature: float, runs: int):
    # Warmup
    print("Warming up…")
    _ = get_llm_response(
        prompt, model=model, base_url=base_url, temperature=temperature
    )
    print("Warmup done.\n")

    times = []
    for i in range(1, runs + 1):
        start = time.perf_counter()
        resp = get_llm_response(
            prompt, model=model, base_url=base_url, temperature=temperature
        )
        duration = time.perf_counter() - start
        times.append(duration)
        # Optionally inspect resp length to compute tokens later
        print(f" Run {i}/{runs}: {duration:.3f} s")

    avg = statistics.mean(times)
    stdev = statistics.stdev(times) if runs > 1 else 0.0
    # Estimate tokens/sec: naive split on whitespace
    token_count = len(resp.split())
    tps = token_count / avg if avg > 0 else 0.0

    print("\n=== Summary ===")
    print(f"Runs:              {runs}")
    print(f"Avg. latency:      {avg:.3f} ± {stdev:.3f} s")
    print(f"Last response tokens: {token_count}")
    print(f"Approx. throughput:   {tps:.1f} tokens/s")


if __name__ == "__main__":
    args = parse_args()
    print(f"Benchmarking Ollama on {args.base_url} using model '{args.model}'")
    print(f"Prompt: “{args.prompt}” | Temp: {args.temperature} | Runs: {args.runs}\n")
    benchmark(
        prompt=args.prompt,
        model=args.model,
        base_url=args.base_url,
        temperature=args.temperature,
        runs=args.runs,
    )
