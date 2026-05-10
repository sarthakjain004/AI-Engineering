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

# =============================================================================
# How temperature works
# =============================================================================
# The model outputs raw scores called LOGITS (one per token in the vocab).
# Logits are FIXED — temperature does not change them.
# Logits go through softmax to become probabilities:
#
#       P(token_i) = exp(logit_i / T) / sum(exp(logit_j / T))
#
# Temperature (T) only enters as the divisor. It reshapes the distribution:
#
#   Low T  (e.g. 0.1) -> logits/T amplify -> top token dominates
#                       distribution gets PEAKY:   ▁▁▁█▁▁▁
#                       near-deterministic output
#
#   T = 1.0           -> logits unchanged -> "natural" distribution
#                                                    ▂▃▅█▅▃▂
#
#   High T (e.g. 2.0) -> logits/T shrink -> gaps between tokens collapse
#                       distribution gets FLAT:    ▅▆▇█▇▆▅
#                       more variety, eventually gibberish
#
#   T = 0  -> mathematical singularity; APIs treat it as argmax (pick top logit)
#   T -> infinity -> uniform distribution (pure random)
#
# Example logits: "Bean"=4.0, "Daily"=2.0, "Cup"=1.0
#   T=0.1  -> Bean ~99.99% | Daily ~0% | Cup ~0%
#   T=1.0  -> Bean ~84%    | Daily ~11% | Cup ~5%
#   T=2.0  -> Bean ~62%    | Daily ~23% | Cup ~15%
#
# Intuition: temperature is a CONTRAST knob on the model's opinion. The model
# always has the same preferences (logits); temperature decides how much we
# respect them vs. flatten them toward chance.
# =============================================================================

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