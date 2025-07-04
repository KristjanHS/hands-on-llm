#!/usr/bin/env python3
"""
Benchmark the Ollama API by sending a chat completion request and measuring the response time.
Uses the OpenAI-compatible /v1/chat/completions endpoint and reports token usage statistics.
"""

import argparse
import time
import statistics
import requests
from phase1.python_code.windows_ip_in_wsl import get_windows_host_ip


def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments for the benchmarking script.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    p = argparse.ArgumentParser(
        description="Benchmark local Ollama via its OpenAI-compatible API with accurate token stats"
    )
    p.add_argument(
        "--host",
        "-H",
        default=get_windows_host_ip() or "localhost",
        help="Ollama API host (default: detected Windows host IP, or localhost if not found)",
        # Uses get_windows_host_ip from windows_ip_in_wsl.py
        # localhost  # WSL ollama host
        # 172.22.208.1  # Windows ollama host
    )
    p.add_argument("--port", "-P", type=int, default=11434, help="Ollama API port (default: 11434)")
    p.add_argument("--model", "-m", default="mistral", help="Model name (default: mistral)")
    p.add_argument(
        "--temperature",
        "-t",
        type=float,
        default=0.0,
        help="Sampling temperature (default: 0.0)",
    )
    p.add_argument(
        "--prompt",
        "-p",
        default=(
            "Please write a long and detailed article about the future of AI in military robotics, "
            "focusing on ethical challenges, technical limitations, and societal impact. "
            "Be as comprehensive as possible."
        ),
        help=("Text prompt to send"),
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
        "--num-predict",
        "-n",
        type=int,
        default=256,
        help="Maximum tokens to generate (num_predict; default: server default)",
    )
    p.add_argument("--runs", "-r", type=int, default=5, help="Number of timed runs (default: 5)")
    return p.parse_args()


def call_chat_completions(args: argparse.Namespace) -> tuple[dict, int, int]:
    """
    Call the Ollama HTTP /v1/chat/completions endpoint and return the parsed JSON and token usage.

    Args:
        args (argparse.Namespace): Parsed command-line arguments.

    Returns:
        tuple: (response JSON, prompt_tokens, completion_tokens)
    """
    url = f"http://{args.host}:{args.port}/v1/chat/completions"
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": args.model,
        "messages": [
            {"role": "system", "content": args.system_prompt},
            {"role": "user", "content": args.prompt},
        ],
        "temperature": args.temperature,
        "max_tokens": args.num_predict,
        "stream": False,
    }

    r = requests.post(url, headers=headers, json=payload)
    r.raise_for_status()
    data = r.json()

    usage = data.get("usage", {})
    pt = usage.get("prompt_tokens", 0)
    ct = usage.get("completion_tokens", 0)
    return data, pt, ct


def benchmark(args: argparse.Namespace) -> None:
    """
    Run the benchmark for the specified LLM model and print summary statistics.

    Args:
        args (argparse.Namespace): Parsed command-line arguments.
    """
    print(
        f"→ Connecting to Ollama-compatible endpoint at "
        f"http://{args.host}:{args.port}/v1/chat/completions"
    )
    print(f"  Model={args.model} | Temp={args.temperature} | Runs={args.runs}\n")

    # Warmup (not timed)
    print("→ Warmup run…")
    _ = call_chat_completions(args)
    print("Warmup complete.\n")

    latencies, prompt_tokens, completion_tokens = [], [], []
    for i in range(1, args.runs + 1):
        t0 = time.perf_counter()
        _, pt, ct = call_chat_completions(args)
        t1 = time.perf_counter()

        latencies.append(t1 - t0)
        prompt_tokens.append(pt)
        completion_tokens.append(ct)

        print(f" Run {i}/{args.runs}: {t1-t0:.3f}s | prompt={pt}, completion={ct}")

    # Compute aggregate stats
    total_time = sum(latencies)
    total_pt = sum(prompt_tokens)
    total_ct = sum(completion_tokens)
    avg = statistics.mean(latencies)
    stdev = statistics.stdev(latencies) if args.runs > 1 else 0.0
    throughput = total_ct / total_time if total_time > 0 else 0.0

    print("\n=== Summary ===")
    print(f"Avg latency:         {avg:.3f} ± {stdev:.3f} s")
    print(f"Total prompt tokens: {total_pt}")
    print(f"Total completion tokens: {total_ct}")
    print(f"Tokens/sec:          {throughput:.1f}")


if __name__ == "__main__":
    args = parse_args()
    benchmark(args)
