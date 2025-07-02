# this script benchmarks the Oobabooga Text-Generation Web UI via its direct HTTP API.
# It sends a completion request to the /v1/completions endpoint and measures the response time,
#!/usr/bin/env python3
import argparse
import time
import statistics
import requests
import os
from phase1.python_code.windows_ip_in_wsl import get_windows_host_ip

# the disabled tokenizer import is left here for reference, but not used in this script
# from transformers import AutoTokenizer

def parse_args():
    p = argparse.ArgumentParser(
        description="Benchmark Oobabooga Text-Generation Web UI via direct HTTP"
    )
    p.add_argument(
        "--host", "-H", default=get_windows_host_ip() or "127.0.0.1",
        help="API host (default: detected Windows host IP, or 127.0.0.1 if not found)"
        # WIN_IP detected dynamically for Windows oobabooga host
        # 127.0.0.1  # WSL oobabooga host
    )
    p.add_argument(
        "--port", "-P", type=int, default=5000,
        help="API port (default: 5000)"
    )
    p.add_argument(
        "--model", "-M", default="mistral",
        help="Model name (default: mistral)"
    )
    p.add_argument(
        "--temperature", "-T", type=float, default=0.0,
        help="Sampling temperature (default: 0.0)"
    )
    p.add_argument(
        "--prompt", "-p", type=str,
        default="Please write a long and detailed article about the future of AI in military robotics, focusing on ethical challenges, technical limitations, and societal impact. Be as comprehensive as possible.",
        help="Text prompt to send"
    )
    p.add_argument(
        "--system-prompt", "-sp",
        default="You are a helpful AI assistant who talks for as long as possible, providing detailed and comprehensive answers to user queries.",
        help="System prompt to use"
    )
    p.add_argument(
        "--max-new-tokens", "-k", type=int, 
        default=254,
        help="Max new tokens per request (default: 254)"
    )
    p.add_argument(
        "--runs", "-r", type=int, default=5,
        help="Number of timed runs (default: 5)"
    )
    return p.parse_args()

def benchmark(args):
    base_url = f"http://{args.host}:{args.port}"
    endpoint = f"{base_url}/v1/completions"

    print(f"→ Connecting to Ooba API at {endpoint}")
    print(f"  Model={args.model} | Temp={args.temperature} | Runs={args.runs}\n")

    # Warmup run (not timed)
    print("→ Warmup run…")
    _ = requests.post(
        endpoint,
        json={
            "model": args.model,
            "prompt": args.prompt + "\n" + args.system_prompt,
            "max_tokens": args.max_new_tokens,
            "temperature": args.temperature
        }
    )
    print("Warmup complete.\n")

    latencies = []
    prompt_tokens = []
    comp_tokens = []

    for i in range(1, args.runs + 1):
        payload = {
            "model": args.model,
            "prompt": args.prompt + "\n" + args.system_prompt,
            "max_tokens": args.max_new_tokens,
            "temperature": args.temperature
        }

        t0 = time.perf_counter()
        response = requests.post(endpoint, json=payload)
        t1 = time.perf_counter()

        ''' Got several errors with this, so disabled for now'
        # check the number of tokens in the response
        tokenizer = AutoTokenizer.from_pretrained("JamesKim/Mistral-7B-v0.3-q4")
        tokens = tokenizer.encode(response, add_special_tokens=False)
        print(len(tokens)) 
        '''

        elapsed = t1 - t0
        latencies.append(elapsed)

        data = response.json()
        usage = data.get("usage", {})
        pt = usage.get("prompt_tokens", 0)
        ct = usage.get("completion_tokens", 0)
        prompt_tokens.append(pt)
        comp_tokens.append(ct)

        print(f" Run {i}/{args.runs}: {elapsed:.3f} s  |  "
              f"prompt_tokens={pt}, completion_tokens={ct}")

    total_time = sum(latencies)
    total_pt = sum(prompt_tokens)
    total_ct = sum(comp_tokens)
    avg = statistics.mean(latencies)
    stdev = statistics.stdev(latencies) if len(latencies) > 1 else 0.0
    throughput = total_ct / total_time if total_time > 0 else 0.0

    print("\n=== Summary ===")
    print(f"Runs:                    {args.runs}")
    print(f"Avg latency:            {avg:.3f} ± {stdev:.3f} s")
    print(f"Total prompt tokens:     {total_pt}")
    print(f"Total completion tokens:{total_ct}")
    print(f"Overall throughput:      {throughput:.1f} tokens/s")

if __name__ == "__main__":
    args = parse_args()
    benchmark(args)
