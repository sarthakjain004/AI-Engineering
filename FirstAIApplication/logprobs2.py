import math
from openai import OpenAI
import os
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

# A more ambiguous classification task
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": "Classify the sentiment as positive, negative, or neutral. "
            "Respond with one word only.",
        },
        {"role": "user", "content": "The product works but the shipping was slow."},
    ],
    logprobs=True,
    top_logprobs=3,
    max_tokens=5,
    temperature=0,
)

first_token = response.choices[0].logprobs.content[0]
print(f"Classification: {first_token.token}")
print(f"Confidence: {math.exp(first_token.logprob) * 100:.1f}%")
print("\nAlternatives:")
for alt in first_token.top_logprobs:
    print(f"  {alt.token}: {math.exp(alt.logprob) * 100:.1f}%")