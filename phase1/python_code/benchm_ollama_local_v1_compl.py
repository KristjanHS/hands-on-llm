# this script benchmarks the Ollama API by sending a chat completion request and measuring the response time, while also collecting token usage statistics.
# It uses the OpenAI-compatible /v1/completions endpoint

#!/usr/bin/env python3
import argparse
import time
import statistics
import requests
from phase1.python_code.windows_ip_in_wsl import get_windows_host_ip


def parse_args():
    p = argparse.ArgumentParser(
        description="Benchmark local Ollama via its OpenAI-compatible API with accurate token stats"
    )
    p.add_argument(
        "--host", "-H",
        default=get_windows_host_ip() or "localhost",
        help="Ollama API host (default: detected Windows host IP, or localhost if not found)"
        # Uses get_windows_host_ip from windows_ip_in_wsl.py
    )
    p.add_argument(
        "--port", "-P",
        type=int,
        default=11434,
        help="Ollama API port (default: 11434)"
    )
    p.add_argument(
        "--model", "-m",
        default="mistral",
        help="Model name (default: mistral)"
    )
    p.add_argument(
        "--temperature", "-t",
        type=float,
        default=0.0,
        help="Sampling temperature (default: 0.0)"
    )
    p.add_argument(
        "--prompt", "-p",
        default="Please write a long and detailed article about the future of AI in military robotics, focusing on ethical challenges, technical limitations, and societal impact. Be as comprehensive as possible.",
        help="Text prompt to send"
    )
    p.add_argument(
        "--system-prompt", "-sp",
        default="You are a helpful AI assistant who talks for as long as possible, providing detailed and comprehensive answers to user queries.",
        help="System prompt to use"
    )
    p.add_argument(
        "--num-predict", "-n",
        type=int,
        default=256,
        help="Maximum tokens to generate (num_predict; default: server default)"
    )
    p.add_argument(
        "--num-ctx", "-ct",
        type=int,
        default=8192,
        help="Maximum tokens in context (num_ctx; default: server default)"
    )
    p.add_argument(
        "--runs", "-r",
        type=int,
        default=5,
        help="Number of timed runs (default: 5)"
    )
    return p.parse_args()


def call_ollama_api(host, port, model, prompt, temperature, num_predict, num_ctx):
    """
    Call the Ollama HTTP /v1/completions endpoint and return the parsed JSON.
    """
    url = f"http://{host}:{port}/v1/completions"
    payload = {
        "model": model,
        "prompt": prompt,
        "temperature": temperature
    }
    if num_predict is not None:
        payload["max_tokens"] = num_predict
    if num_ctx is not None:
        payload["context_window"] = num_ctx

    resp = requests.post(url, json=payload)
    resp.raise_for_status()
    return resp.json()


def benchmark(args):
    print(f"→ Connecting to Ollama at http://{args.host}:{args.port}")
    print(f"  Model={args.model} | Temp={args.temperature} | Runs={args.runs}\n")

    # Warmup (not timed)
    print("→ Warmup run…")
    call_ollama_api(
        args.host, args.port,
        args.model, 
        args.prompt + "\n" + args.system_prompt,
        args.temperature,
        args.num_predict, 
        args.num_ctx
    )
    print("Warmup complete.\n")

    latencies = []
    prompt_tokens = []
    completion_tokens = []

    for i in range(1, args.runs + 1):
        t0 = time.perf_counter()
        data = call_ollama_api(
            args.host, args.port,
            args.model, args.prompt + "\n" + args.system_prompt,
            args.temperature,
            args.num_predict, 
            args.num_ctx
        )
        t1 = time.perf_counter()

        elapsed = t1 - t0
        latencies.append(elapsed)

        usage = data.get("usage", {})
        pt = usage.get("prompt_tokens", 0)
        ct = usage.get("completion_tokens", 0)
        prompt_tokens.append(pt)
        completion_tokens.append(ct)

        print(f" Run {i}/{args.runs}: {elapsed:.3f} s  |  "
              f"prompt_tokens={pt}, completion_tokens={ct}")

    total_time = sum(latencies)
    total_pt = sum(prompt_tokens)
    total_ct = sum(completion_tokens)
    avg = statistics.mean(latencies)
    stdev = statistics.stdev(latencies) if len(latencies) > 1 else 0.0
    throughput = total_ct / total_time if total_time > 0 else 0.0

    print("\n=== Summary ===")
    print(f"Runs:                    {args.runs}")
    print(f"Avg. latency:            {avg:.3f} ± {stdev:.3f} s")
    print(f"Total prompt tokens:     {total_pt}")
    print(f"Total completion tokens: {total_ct}")
    print(f"Overall throughput:      {throughput:.1f} tokens/s")


if __name__ == "__main__":
    args = parse_args()
    benchmark(args)
