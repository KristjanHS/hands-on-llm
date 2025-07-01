#!/usr/bin/env python3
import argparse
import time
import statistics
import requests
# from ooba_api import OobaApiClient, Parameters, LlamaInstructPrompt

def parse_args():
    p = argparse.ArgumentParser(
        description="Benchmark Ooba-Booga TextGen Web UI inference performance (with warmup)"
    )
    p.add_argument(
        "--host", "-H", 
        default="127.0.0.1",  # WSL oobabooga host
        help="API host (default: 127.0.0.1)"
    )
    p.add_argument(
        "--port", "-P", type=int, 
        default=5000,
        help="API port (default: 5000)"
    )
    p.add_argument(
        "--model", "-m", 
        default="mistral",
        help="Model name to load (e.g. mistral)"
    )
    p.add_argument(
        "--temperature", "-t", type=float,
        default=0.0,
        help="Sampling temperature (default: 0.0)"
    )
    p.add_argument(
        "--prompt", "-p", 
        default="Hello, how are you?",
        help="Text prompt to send"
    )
    p.add_argument(
        "--system-prompt", "-s", 
        default="",
        help="Optional system prompt for chat endpoints"
    )
    p.add_argument(
        "--max-tokens", "-k", type=int, 
        default=64,
        help="Max new tokens per request"
    )
    p.add_argument(
        "--runs", "-r", type=int, 
        default=5,
        help="Number of timed runs (default: 5)"
    )
    return p.parse_args()

def call_api(host, port, model, prompt, max_tokens, temperature):
    url = f"http://{host}:{port}/v1/completions"
    data = {
        "model": model,
        "prompt": prompt,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    r = requests.post(url, json=data)
    r.raise_for_status()
    return r.json()["choices"][0]["text"]

def benchmark(args):
    print("→ Warmup run…")
    _ = call_api(args.host, args.port, args.model, args.prompt, args.max_tokens, args.temperature)
    print("Warmup complete.\n")

    times, last = [], ""
    for i in range(1, args.runs+1):
        t0 = time.perf_counter()
        last = call_api(args.host, args.port, args.model, args.prompt, args.max_tokens, args.temperature)
        dt = time.perf_counter() - t0
        times.append(dt)
        print(f" Run {i}/{args.runs}: {dt:.3f} s")

    avg = statistics.mean(times)
    stdev = statistics.stdev(times) if len(times)>1 else 0.0
    tokens = len(last.split())
    tps = tokens/avg if avg>0 else 0.0

    print("\n=== Summary ===")
    print(f"Runs:                {args.runs}")
    print(f"Avg latency:         {avg:.3f} ± {stdev:.3f} s")
    print(f"Last response tokens:{tokens}")
    print(f"Throughput:          {tps:.1f} tokens/s")

if __name__ == "__main__":
    args = parse_args()
    print(f"Benchmarking {args.model} on {args.host}:{args.port} | temp={args.temperature} | runs={args.runs}\n")
    benchmark(args)

'''
def benchmark(client, prompt_obj, params, runs):
    # --- Warmup ---
    print("Warming up…")
    _ = client.instruct(prompt_obj, parameters=params)
    print("Warmup complete.\n")

    # --- Timed runs ---
    times = []
    last_response = None
    for i in range(1, runs + 1):
        t0 = time.perf_counter()
        last_response = client.instruct(prompt_obj, parameters=params)
        t1 = time.perf_counter()
        delta = t1 - t0
        times.append(delta)
        print(f" Run {i}/{runs}: {delta:.3f} s")

    # --- Summary ---
    avg = statistics.mean(times)
    stdev = statistics.stdev(times) if len(times) > 1 else 0.0
    # naive token estimate
    token_count = len(last_response.content.split())
    tps = token_count / avg if avg > 0 else 0.0

    print("\n=== Summary ===")
    print(f"Runs:                {runs}")
    print(f"Avg. latency:        {avg:.3f} ± {stdev:.3f} s")
    print(f"Last response tokens:{token_count}")
    print(f"Approx. throughput:  {tps:.1f} tokens/s\n")

def main():
    args = parse_args()
    base_url = f"http://{args.host}:{args.port}"
    client = OobaApiClient(url=base_url)
    print(f"Connected to Ooba API at {base_url}")
    print(f"Prompt: “{args.prompt}” | Max-new-tokens: {args.max_new_tokens} | Runs: {args.runs}\n")

    prompt_obj = LlamaInstructPrompt(
        system_prompt=args.system_prompt,
        prompt=args.prompt
    )
    params = Parameters(max_new_tokens=args.max_new_tokens)

    benchmark(client, prompt_obj, params, args.runs)

if __name__ == "__main__":
    main()
'''