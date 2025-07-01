#!/usr/bin/env python3
import argparse
import time
import statistics
import requests

def parse_args():
    p = argparse.ArgumentParser(
        description="Benchmark Oobabooga Text-Generation Web UI via direct HTTP"
    )
    p.add_argument(
        "--host", "-H", default="127.0.0.1",
        help="API host (default: 127.0.0.1)"
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
        "--prompt", "-p", default="Hello, how are you?",
        help="Text prompt to send"
    )
    p.add_argument(
        "--max-new-tokens", "-k", type=int, default=64,
        help="Max new tokens per request (default: 64)"
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
            "prompt": args.prompt,
            "max_tokens": args.max_new_tokens,
            "temperature": args.temperature
        }
    )
    print("Warmup complete.\n")

    latencies = []
    comp_tokens = []

    for i in range(1, args.runs + 1):
        payload = {
            "model": args.model,
            "prompt": args.prompt,
            "max_tokens": args.max_new_tokens,
            "temperature": args.temperature
        }

        t0 = time.perf_counter()
        response = requests.post(endpoint, json=payload)
        t1 = time.perf_counter()

        elapsed = t1 - t0
        latencies.append(elapsed)

        data = response.json()
        usage = data.get("usage", {})
        ct = usage.get("completion_tokens", 0)
        comp_tokens.append(ct)

        print(f" Run {i}/{args.runs}: {elapsed:.3f} s | completion_tokens={ct}")

    total_time = sum(latencies)
    total_ct = sum(comp_tokens)
    avg = statistics.mean(latencies)
    stdev = statistics.stdev(latencies) if len(latencies) > 1 else 0.0
    throughput = total_ct / total_time if total_time > 0 else 0.0

    print("\n=== Summary ===")
    print(f"Runs:                    {args.runs}")
    print(f"Avg latency:            {avg:.3f} ± {stdev:.3f} s")
    print(f"Total completion tokens:{total_ct}")
    print(f"Overall throughput:      {throughput:.1f} tokens/s")

if __name__ == "__main__":
    args = parse_args()
    benchmark(args)
