#!/usr/bin/env python3
import argparse
import time
import statistics
from langchain_ollama import ChatOllama
from langchain.schema import AIMessage


def get_llm_response(
    prompt: str,
    *,
    model: str = "mistral",
    base_url: str = "http://localhost:11434",
    system_prompt: str = (
        "You are a helpful but terse AI assistant who gets straight to the point."
    ),
    temperature: float = 0.0,
    num_predict: int = None,
    num_ctx: int = None,
) -> str:
    """
    Send `prompt` to a local Ollama model via LangChain's ChatOllama,
    supporting num_predict and num_ctx settings.
    """
    llm = ChatOllama(
        model=model,
        base_url=base_url,
        system=system_prompt,
        temperature=temperature,
        num_predict=num_predict,
        num_ctx=num_ctx,
        streaming=False,  # one-shot response, no token loop
    )
    message: AIMessage = llm.invoke(prompt)
    return message.content.strip()


def parse_args():
    p = argparse.ArgumentParser(
        description="Benchmark local Ollama inference with num_predict & num_ctx"
    )
    p.add_argument(
        "--prompt", "-p",
        default="Hello, how are you?",
        help="Text prompt to send"
    )
    p.add_argument(
        "--model", "-m",
        default="mistral",
        help="Ollama model name (default: mistral)"
    )
    p.add_argument(
        "--base-url", "-b",
    #    default="http://localhost:11434",  # WSL ollama host
        default="http://172.22.208.1:11434",  # Windows ollama host
        help="Base URL for local Ollama server"
    )
    p.add_argument(
        "--temperature", "-t",
        type=float,
        default=0.0,
        help="Sampling temperature (default: 0.0)"
    )
    p.add_argument(
        "--num-predict", "-n",
        type=int,
        default=None,
        help="Maximum tokens to generate (num_predict, default: None=infinite)"
    )
    p.add_argument(
        "--num-ctx", "-c",
        type=int,
        default=None,
        help="Context window size (num_ctx, default: server default)"
    )
    p.add_argument(
        "--runs", "-r",
        type=int,
        default=5,
        help="Number of timed runs (default: 5)"
    )
    return p.parse_args()


def benchmark(
    prompt: str,
    model: str,
    base_url: str,
    system_prompt: str,
    temperature: float,
    num_predict: int,
    num_ctx: int,
    runs: int
):
    # Warmup
    print("→ Warmup run (not timed)…")
    _ = get_llm_response(
        prompt,
        model=model,
        base_url=base_url,
        system_prompt=system_prompt,
        temperature=temperature,
        num_predict=num_predict,
        num_ctx=num_ctx,
    )
    print("Warmup complete.\n")

    times = []
    last_resp = None
    for i in range(1, runs + 1):
        start = time.perf_counter()
        last_resp = get_llm_response(
            prompt,
            model=model,
            base_url=base_url,
            system_prompt=system_prompt,
            temperature=temperature,
            num_predict=num_predict,
            num_ctx=num_ctx,
        )
        duration = time.perf_counter() - start
        times.append(duration)
        print(f" Run {i}/{runs}: {duration:.3f} s")

    avg = statistics.mean(times)
    stdev = statistics.stdev(times) if runs > 1 else 0.0
    # Estimate tokens by splitting last response
    token_count = len(last_resp.split())
    tps = token_count / avg if avg > 0 else 0.0

    print("\n=== Summary ===")
    print(f"Runs:                {runs}")
    print(f"Avg. latency:        {avg:.3f} ± {stdev:.3f} s")
    print(f"Last response tokens:{token_count}")
    print(f"Approx. throughput:  {tps:.1f} tokens/s")


if __name__ == "__main__":
    args = parse_args()
    print(
        f"Benchmarking Ollama on {args.base_url} using model '{args.model}'"
    )
    print(
        f"Prompt: “{args.prompt}” | Temp: {args.temperature} | "
        f"num_predict: {args.num_predict} | num_ctx: {args.num_ctx} | Runs: {args.runs}\n"
    )
    benchmark(
        prompt=args.prompt,
        model=args.model,
        base_url=args.base_url,
        system_prompt=(
            "You are a helpful but terse AI assistant who gets straight to the point."
        ),
        temperature=args.temperature,
        num_predict=args.num_predict,
        num_ctx=args.num_ctx,
        runs=args.runs
    )
