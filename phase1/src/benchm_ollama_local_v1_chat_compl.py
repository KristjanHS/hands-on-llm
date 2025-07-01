# this script benchmarks the Ollama API by sending a chat completion request and measuring the response time, while also collecting token usage statistics.
# It uses the OpenAI-compatible /v1/chat/completions endpoint

#!/usr/bin/env python3
import argparse
import time
import statistics
import requests



def parse_args():
    p = argparse.ArgumentParser(
        description="Benchmark local Ollama via its OpenAI-compatible API with accurate token stats"
    )
    p.add_argument(
        "--host", "-H",
        default="172.22.208.1",
        help="Ollama API host (default: localhost)"
        # localhost  # WSL ollama host
        # 172.22.208.1  # Windows ollama host
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
        "--runs", "-r",
        type=int,
        default=5,
        help="Number of timed runs (default: 5)"
    )
    return p.parse_args()

#!/usr/bin/env python3
import argparse
import time
import statistics
import requests

''' the shorter version of the parse_args function
def parse_args():
    p = argparse.ArgumentParser(
        description="Benchmark local Ollama via OpenAI-compatible /v1/chat/completions API with token stats"
    )
    p.add_argument("--host", "-H", default="localhost", help="Ollama API host (default: localhost)")
    p.add_argument("--port", "-P", type=int, default=11434, help="Ollama API port (default: 11434)")
    p.add_argument("--model", "-m", default="mistral", help="Model name (default: mistral)")
    p.add_argument("--temperature", "-t", type=float, default=0.0, help="Sampling temperature")
    p.add_argument("--prompt", "-p", default="Please write a long and detailed article about the future of AI in military robotics, focusing on ethical challenges, technical limitations, and societal impact. Be as comprehensive as possible.", help="Text prompt to send")
    p.add_argument("--system-prompt", "-sp", default="You are a helpful AI assistant who talks for as long as possible, providing detailed and comprehensive answers to user queries.", help="System prompt to use")
    p.add_argument("--num-predict", "-n", type=int, default=256, help="Maximum tokens to generate (default: 256)")
    p.add_argument("--runs", "-r", type=int, default=5, help="Number of timed runs (default: 5)")
    return p.parse_args()
'''

def call_chat_completions(args):
    url = f"http://{args.host}:{args.port}/v1/chat/completions"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "model": args.model,
        "messages": [
            {"role": "system", "content": args.system_prompt},
            {"role": "user", "content": args.prompt}
        ],
        "temperature": args.temperature,
        "max_tokens": args.num_predict,
        "stream": False
    }

    r = requests.post(url, headers=headers, json=payload)
    r.raise_for_status()
    data = r.json()

    usage = data.get("usage", {})
    pt = usage.get("prompt_tokens", 0)
    ct = usage.get("completion_tokens", 0)
    return data, pt, ct


def benchmark(args):
    print(f"→ Connecting to Ollama-compatible endpoint at http://{args.host}:{args.port}/v1/chat/completions")
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

    print(f"\n=== Summary ===")
    print(f"Avg latency:         {avg:.3f} ± {stdev:.3f} s")
    print(f"Total prompt tokens: {total_pt}")
    print(f"Total completion tokens: {total_ct}")
    print(f"Tokens/sec:          {throughput:.1f}")


if __name__ == "__main__":
    args = parse_args()
    benchmark(args)
