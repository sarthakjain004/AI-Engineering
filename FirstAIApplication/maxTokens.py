from openai import OpenAI
import os
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

# Short limit - will likely cut off
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Explain how a hash table works."}],
    max_tokens=50,
)

print(response.choices[0].message.content)
print(f"Finish reason: {response.choices[0].finish_reason}")
# Likely prints: "length" - the model wanted to say more

# Generous limit - model stops naturally
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Explain how a hash table works."}],
    max_tokens=2000,
)

print(f"Finish reason: {response.choices[0].finish_reason}")
# Likely prints: "stop" - the model finished on its own
print(f"Tokens used: {response.usage.completion_tokens}")
# The model probably used far fewer than 2000