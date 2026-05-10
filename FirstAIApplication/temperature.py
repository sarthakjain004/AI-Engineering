from dotenv import load_dotenv
import os
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()
open_router_api_key = os.getenv("OPENROUTER_API_KEY")

client  = OpenAI(
    api_key=open_router_api_key,
    base_url="https://openrouter.ai/api/v1",
)

prompt = "Suggest a good name for a coffee shop"

temperatures = [0.0, 0.3, 0.7, 1.0, 1.5, 2.0]

for temp in temperatures:
    print(f"Temperature: {temp}")
    print("=" * 40)
    for i in range(3):
        try:
            response = client.chat.completions.create(
                model = "gpt-4o-mini",
                messages = [
                    { "role": "user", "content": prompt }
                ],
                temperature = temp,
                max_tokens = 50
            )
            print(f"Response {i+1}: {response.choices[0].message.content}")
        except Exception as e:
            print(f"Error occurred: {e}")