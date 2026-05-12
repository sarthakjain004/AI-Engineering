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

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": "What is the capital of France? Answer in one word."}
    ],
    logprobs=True,
    top_logprobs=3,
    max_tokens=10,
    temperature=0,
)

# Inspect token-level probabilities
for token_info in response.choices[0].logprobs.content:
    prob = math.exp(token_info.logprob) * 100
    print(f"Token: '{token_info.token}' | Probability: {prob:.1f}%")

    # Show alternatives the model considered
    for alt in token_info.top_logprobs:
        alt_prob = math.exp(alt.logprob) * 100
        print(f"  Alternative: '{alt.token}' | {alt_prob:.1f}%")