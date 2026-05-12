from openai import OpenAI
import os
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

# Use stop sequences to extract just a function name
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": "You are a code assistant. When asked to name a function, "
            "respond with just the function name, nothing else.",
        },
        {
            "role": "user",
            "content": "What should I name a function that validates compound fields in a data structure?",
        },
    ],
    stop=["(", "\n", " "],  # Stop at parenthesis, newline, or space
    max_tokens=50,
)

print(response.choices[0].message.content)
# Output: "validate_email" (stops before any extra text)