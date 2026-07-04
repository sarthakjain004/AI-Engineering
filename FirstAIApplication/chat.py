# Interactive terminal chatbot for the local Qwen model — WITH conversation memory.
#
# Start the server first (separate terminal):
#   cd "/Users/sarthakjain/Learning/AI Engineering"
#   HF_HUB_OFFLINE=1 .venv/bin/python -m mlx_lm.server --model mlx-community/Qwen3.6-35B-A3B-6bit --port 8080
# Then run this:
#   .venv/bin/python FirstAIApplication/chat.py
#
# Commands while chatting:  exit / quit  -> leave    |    reset -> wipe memory

from openai import OpenAI

MODEL = "mlx-community/Qwen3.6-35B-A3B-6bit"
CONTEXT_LIMIT = 262_144  # this model's max context window, in tokens

client = OpenAI(api_key="local", base_url="http://localhost:8080/v1")

# THE conversation. We resend this whole list every turn — that's the model's
# "memory". The API itself remembers nothing between calls.
messages = [
    {"role": "system", "content": "You are a helpful, concise local assistant."}
]

print("Local Qwen chat — type 'exit' to quit, 'reset' to clear memory.\n")

while True:
    try:
        user = input("you ▸ ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\nbye!")
        break

    if not user:
        continue
    if user.lower() in {"exit", "quit"}:
        print("bye!")
        break
    if user.lower() == "reset":
        messages = messages[:1]          # keep only the system prompt
        print("(memory cleared)\n")
        continue

    messages.append({"role": "user", "content": user})

    # Stream the reply so it types out live, like a real chatbot.
    print("bot ▸ ", end="", flush=True)
    reply, usage = "", None
    stream = client.chat.completions.create(
        model=MODEL,
        max_tokens=1000,             # generous: this is a "thinking" model
        messages=messages,           # <-- the full history goes every time
        stream=True,
        stream_options={"include_usage": True},
    )
    for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content:
            piece = chunk.choices[0].delta.content
            reply += piece
            print(piece, end="", flush=True)
        if chunk.usage:              # arrives in the final chunk
            usage = chunk.usage
    print()

    # Save the assistant's turn so the NEXT request includes it = memory.
    messages.append({"role": "assistant", "content": reply})

    # Visualize how full the context window is getting.
    if usage:
        print(f"   [context: {usage.total_tokens:,} / {CONTEXT_LIMIT:,} tokens"
              f" · {len(messages)} messages]\n")
    else:
        print(f"   [{len(messages)} messages in memory]\n")
