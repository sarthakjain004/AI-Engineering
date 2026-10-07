# Talk to the LOCAL model server running on port 1234 (OpenAI-compatible API).
#
# The server should already be running and ready at http://127.0.0.1:1234
# No API key needed — using local inference.

from openai import OpenAI

client = OpenAI(
    api_key="local",
    base_url="http://127.0.0.1:1234/v1",
)

response = client.chat.completions.create(
    model="qwen/qwen3.6-35b-a3b",
    max_tokens=1500,  # thinking model: reasoning tokens count toward the cap
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
