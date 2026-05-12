from openai import OpenAI
import os
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "What is a binary search tree?"}],
    max_tokens=500,
)

usage = response.usage
print(f"Input tokens:  {usage.prompt_tokens}")
print(f"Output tokens: {usage.completion_tokens}")
print(f"Total tokens:  {usage.total_tokens}")

# Calculate actual cost for openai/gpt-oss-120b ($0.15 input / $0.60 output per 1M tokens)
input_cost = (usage.prompt_tokens / 1_000_000) * 0.15
output_cost = (usage.completion_tokens / 1_000_000) * 0.60
print(f"Actual cost:   ${input_cost + output_cost:.6f}")