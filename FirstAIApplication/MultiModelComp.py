from dotenv import load_dotenv
import os
import time
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()
open_router_api_key = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
    api_key=open_router_api_key,
    base_url="https://openrouter.ai/api/v1",
)

def call_model(model: str, prompt:str, system_prompt: str = 
               "You are a helpful assistant.") -> dict:
    """Call any model with OpenAI's API and return the response with metadata"""
    start_time = time.time()
    response = client.chat.completions.create(
        model = model,
        messages = [
            { "role": "system", "content": system_prompt},
            { "role": "user", "content": prompt }
        ]
    )
    elapsed = time.time() - start_time
    return {
        "model": model,
        "response": response.choices[0].message.content,
        "input_tokens": response.usage.prompt_tokens,
        "output_tokens": response.usage.completion_tokens,
        "latency_seconds": round(elapsed, 2)
    }


def compare_models(prompt: str, system_prompt: str = "You are a helpful assistant.") -> None:
    """Send same prompt to multiple models and compare results."""
    models = [
        "openai/gpt-oss-120b",
        "google/gemma-3-27b-it",
        "meta-llama/llama-3.1-8b-instruct",
    ]
    print(f"Prompt: {prompt} \n")
    print("=" * 80)
    results = []
    for model in models:
        try:
            result = call_model(model, prompt, system_prompt)
            results.append(result)
            print(f"Model: {result['model']}")
            print(f"Response: {result['response']}")
            print(f"Input Tokens: {result['input_tokens']}")
            print(f"Output Tokens: {result['output_tokens']}")
            print(f"Latency (s): {result['latency_seconds']}")
            print("-" * 80)
        except Exception as e:
            print(f"Error calling model {model}: {e}")
            print("-" * 80)

    if results:
        print("=" * 80)
        print("\nComparison Summary:")
        print(f"{'Model':<50} {'Latency':>10} {'Input':>8} {'Output':>8}")
        print("-" * 80)
        for r in results:
            print(f"{r['model']:<50} {r['latency_seconds']:>8.2f}s "
                  f"{r['input_tokens']:>8} {r['output_tokens']:>8}")


if __name__ == "__main__":
    prompt = "Explain the difference between boiling point and melting point."
    system_prompt = "You are a helpful assistant that provides concise scientific explanations."
    compare_models(prompt, system_prompt)
