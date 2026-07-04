# Talk to the LOCAL Qwen3.6-35B-A3B (MLX 6-bit) model — no internet, no API cost.
#
# 1) Start the local server in a separate terminal (serves an OpenAI-compatible API):
#      cd "/Users/sarthakjain/Learning/AI Engineering"
#      .venv/bin/python -m mlx_lm.server --model mlx-community/Qwen3.6-35B-A3B-6bit --port 8080
#
# 2) Run this file:
#      .venv/bin/python FirstAIApplication/local_model.py
#
# Same OpenAI client as the rest of the project — only base_url changes.

from openai import OpenAI

# A local server needs no real key; any non-empty string is accepted.
client = OpenAI(
    api_key="local",
    base_url="http://localhost:8080/v1",
)

response = client.chat.completions.create(
    model="mlx-community/Qwen3.6-35B-A3B-6bit",
    max_tokens=500,  # explicit cap, per project convention
    messages=[
        {"role": "system", "content": "You are a helpful local assistant. Be concise."},
        {"role": "user", "content": "In one sentence, what is mixture-of-experts in an LLM?"},
    ],
)

answer = response.choices[0].message.content
print(answer)

# mlx_lm.server also reports token usage, just like a hosted API.
if response.usage:
    print("Total tokens: ", response.usage.total_tokens)
    print("Input tokens: ", response.usage.prompt_tokens)
    print("Output tokens:", response.usage.completion_tokens)
