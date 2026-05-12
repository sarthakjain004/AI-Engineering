import tiktoken
import os
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

# Pricing per 1M tokens (input, output) — OpenRouter model name format
MODEL_PRICING = {
    "openai/gpt-4o-mini":                       {"input": 2.50,  "output": 10.00, "encoding": "o200k_base"},
    "openai/gpt-oss-120b":                  {"input": 0.15,  "output":  0.60, "encoding": "o200k_base"},
    "anthropic/claude-haiku-4-5-20251001": {"input": 0.80,  "output":  4.00, "encoding": "cl100k_base"},
    "google/gemini-2.0-flash-001":         {"input": 0.075, "output":  0.30, "encoding": "cl100k_base"},
    "meta-llama/llama-3.1-8b-instruct":    {"input": 0.05,  "output":  0.08, "encoding": "cl100k_base"},
}


def count_tokens(text: str, model: str = "gpt-4o-mini") -> int:
    """Count the number of tokens in a text string."""
    encoding_name = MODEL_PRICING[model]["encoding"]
    encoder = tiktoken.get_encoding(encoding_name)
    return len(encoder.encode(text))


def estimate_cost(
    input_text: str,
    model: str = "gpt-4o-mini",
    estimated_output_tokens: int = 500,
) -> dict:
    """Estimate the cost of an API call."""
    input_tokens = count_tokens(input_text, model)
    pricing = MODEL_PRICING[model]

    input_cost = (input_tokens / 1_000_000) * pricing["input"]
    output_cost = (estimated_output_tokens / 1_000_000) * pricing["output"]
    total_cost = input_cost + output_cost

    return {
        "model": model,
        "input_tokens": input_tokens,
        "estimated_output_tokens": estimated_output_tokens,
        "input_cost": f"${input_cost:.6f}",
        "output_cost": f"${output_cost:.6f}",
        "total_cost": f"${total_cost:.6f}",
    }


# Example usage
prompt = "Explain the differences between SQL and NoSQL databases in detail."

for model in ["openai/gpt-4o-mini", "openai/gpt-oss-120b"]:
    result = estimate_cost(prompt, model=model, estimated_output_tokens=1000)
    print(f"\n{model}:")
    for key, value in result.items():
        print(f"  {key}: {value}")