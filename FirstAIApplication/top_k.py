from openai import OpenAI
import os
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

# Top-k sampling: only consider the top 40 tokens at each step
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Write a haiku about databases."}],
    extra_body={"top_k": 40},  # OpenRouter passes this to supported models
)

print(response.choices[0].message.content)