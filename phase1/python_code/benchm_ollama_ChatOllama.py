#!/usr/bin/env python3
# This script benchmarks the Ollama API by sending a chat completion request
# and measuring the response time, while also collecting token usage statistics.
# It uses the get_llm_response function from helper_functions.py to interact with a
# local Ollama server.
# The endpoint is the OpenAI-compatible /v1/chat/completions API.

import argparse, json
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
        "--prompt",
        "-p",
        default=(
            "Please write a long and detailed article about the future of AI in military robotics, "
            "focusing on ethical challenges, technical limitations, and societal impact. "
            "Be as comprehensive as possible."
        ),
        help="Text prompt to send",
    )
    p.add_argument(
        "--model",
        "-m",
        default="mistral",
        help="Ollama model name (default: mistral)",
    )
    p.add_argument(
        "--system-prompt",
        "-sp",
        default=(
            "You are a helpful AI assistant who talks for as long as possible, providing detailed "
            "and comprehensive answers to user queries."
        ),
        help="System prompt to use",
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
        "--num-predict",
        "-n",
        type=int,
        default=256,  # The user is getting 125 tokens, which is different from both.
        help="Maximum tokens to generate (num_predict; default: 256)",
    )
    p.add_argument("--runs", "-r", type=int, default=5, help="Number of timed runs (default: 5)")
    return p.parse_args()


def _get_token_counts(response: any) -> tuple[int, int]:
    """Extracts prompt and completion token counts from a LangChain AIMessage.

    Args:
        response: The response object from `get_llm_response`.

    Returns:
        A tuple containing (prompt_tokens, completion_tokens).
        Returns (-1, -1) if token counts cannot be determined.
    """
    if hasattr(response, "usage_metadata") and response.usage_metadata is not None:
        usage = response.usage_metadata
        prompt_tokens = usage.get("input_tokens", -1)
        completion_tokens = usage.get("output_tokens", -1)
        return prompt_tokens, completion_tokens

    print(f"Unexpected response format: {type(response)}, cannot count tokens accurately.")
    return -1, -1


def benchmark(
    prompt: str,
    model: str,
    base_url: str,
    temperature: float,
    runs: int,
    num_predict: int,
    system_prompt: str,
):
    # Warmup
    print("Warming up…")
    # the stream parameter is
    _ = get_llm_response(
        prompt,
        model=model,
        system_prompt=system_prompt,
        base_url=base_url,
        temperature=temperature,
        num_predict=num_predict,
    )
    print("Warmup done.\n")

    times = []
    prompt_token_counts = []
    completion_token_counts = []
    for i in range(1, runs + 1):  # retry logic
        start = time.perf_counter()
        streamed_resp = get_llm_response(
            prompt,
            model=model,
            system_prompt=system_prompt,
            base_url=base_url,
            temperature=temperature,
            num_predict=num_predict,
            stream=True,
        )
        end = time.perf_counter()
        duration = end - start
        times.append(duration)

        prompt_tokens, completion_tokens = _get_token_counts(streamed_resp)
        if prompt_tokens != -1 and completion_tokens != -1:
            prompt_token_counts.append(prompt_tokens)
            completion_token_counts.append(completion_tokens)
            print(
                f"Run {i}/{runs}: {duration:.3f} s, prompt_tokens={prompt_tokens}, completion_tokens={completion_tokens}"
            )
        else:
            print(f"Run {i}/{runs}: {duration:.3f} s, token count failed.")

    if not times or not completion_token_counts:
        print("\nNo successful runs with token counts to report.")
        return

    avg_latency = statistics.mean(times)
    stdev_latency = statistics.stdev(times) if len(times) > 1 else 0.0
    total_prompt_tokens = sum(prompt_token_counts)
    total_completion_tokens = sum(completion_token_counts)
    total_tokens = total_prompt_tokens + total_completion_tokens
    total_time = sum(times)
    avg_throughput_completion = total_completion_tokens / total_time if total_time > 0 else 0.0
    avg_throughput_total = total_tokens / total_time if total_time > 0 else 0.0

    print("\n=== Summary ===")
    print(f"Runs completed:      {len(completion_token_counts)}/{runs}")
    print(f"Avg. latency:        {avg_latency:.3f} ± {stdev_latency:.3f} s")
    print(f"Total prompt tokens:     {total_prompt_tokens}")
    print(f"Total completion tokens: {total_completion_tokens}")
    print(f"Total tokens (all):      {total_tokens}")
    print(f"Avg. throughput:     {avg_throughput_completion:.1f} tokens/s (completion tokens)")
    print(f"Avg. throughput:     {avg_throughput_total:.1f} tokens/s (total tokens)")


if __name__ == "__main__":
    args = parse_args()
    print(
        f"Benchmarking Ollama on {args.base_url} using model '{args.model}' with max {args.num_predict} tokens"
    )
    print(f"Prompt: “{args.prompt}” | Temp: {args.temperature} | Runs: {args.runs}\n")
    benchmark(
        prompt=args.prompt,
        model=args.model,
        base_url=args.base_url,
        temperature=args.temperature,
        runs=args.runs,
        num_predict=args.num_predict,
        system_prompt=args.system_prompt,
    )
