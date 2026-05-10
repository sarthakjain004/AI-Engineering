from dotenv import load_dotenv
import os
import tiktoken
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

open_router_api_key = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
    api_key=open_router_api_key,
    base_url="https://openrouter.ai/api/v1",
)

prompt = "Explain the difference between boiling point and melting point."
encoding = tiktoken.encoding_for_model("gpt-4o")
tokens = encoding.encode(prompt)
print(len(tokens))

response = client.chat.completions.create(
    model="gpt-4o",
    max_tokens=500,
    messages=[
        {
            "role": "system",
            "content": "No matter what u will be asked, always respond with a joke."
        },
        {
            "role": "user",
            "content": "Where is Andorra?"
        }
    ]
)

answer = response.choices[0].message.content
print(answer)
print("Tokens used in this call: ", response.usage.total_tokens)
# input tokens below
print("Input tokens used in this call: ", response.usage.prompt_tokens)
# output tokens below
print("Output tokens used in this call: ", response.usage.completion_tokens)

print(response)