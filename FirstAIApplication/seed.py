from openai import OpenAI
import os
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

# Same seed produces the same output
# It initializes the random number generator used during sampling, 
# so the model follows the same "path" through its probability distributions.

# In practice short outputs may be identical across runs with the same seed, while longer outputs may have more variation but still share core similarities.
for i in range(3):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Suggest a name for a coffee shop."}],
        temperature=0.7,
        seed=42,
        max_tokens=50,
    )
    print(f"Fingerprint of output: {response.system_fingerprint}")
    #  If two responses have the same fingerprint and seed, they should be identical
    # Note: fingerprint is a hash of the output content, so different outputs will have different fingerprints.
    print(f"Run {i+1}: {response.choices[0].message.content}")