from openai import OpenAI
import os
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

prompt = "Write a 200-word essay about the benefits of exercise."

# No penalties - may repeat phrases
response_default = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
    temperature=1.0,
    max_tokens=300,
)

# High frequency penalty - reduces word repetition
response_freq = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
    temperature=1.0,
    frequency_penalty=1.5,
    max_tokens=300,
)

# High presence penalty - encourages new topics
response_pres = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
    temperature=1.0,
    presence_penalty=1.5,
    max_tokens=300,
)

print("=== Default ===")
print(response_default.choices[0].message.content)
print("\n=== Frequency Penalty 1.5 ===")
print(response_freq.choices[0].message.content)
print("\n=== Presence Penalty 1.5 ===")
print(response_pres.choices[0].message.content)