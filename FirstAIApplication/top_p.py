from dotenv import load_dotenv
import os
from openai import OpenAI, RateLimitError, APITimeoutError, APIConnectionError
# Load environment variables from .env file
load_dotenv()
open_router_api_key = os.getenv("OPENROUTER_API_KEY")
client  = OpenAI(
    api_key=open_router_api_key,
    base_url="https://openrouter.ai/api/v1",
)

# =============================================================================
# How top_p (nucleus sampling) works
# =============================================================================
# Where temperature reshapes the WHOLE probability distribution, top_p
# TRUNCATES it:
#   1. Sort token probabilities high -> low
#   2. Add them up until the cumulative sum exceeds p
#   3. Discard everything below the cutoff, renormalize, sample from what's left
#
# Effect:
#   top_p = 0.3  -> only top ~30% probability mass eligible -> very narrow
#   top_p = 0.7  -> wider pool, tail options become reachable
#   top_p = 1.0  -> nothing truncated (still weighted by probability)
#   top_p = 0.0  -> DEGENERATE (cumulative <= 0 keeps nothing); behavior varies
#                   by provider. Don't use it -- use 0.1 or temperature=0 instead.
#
# Observed run with prompt that excluded "brew/bean/grind" puns:
#   top_p=0.0 -> 3 different "Whispering ___" variants (degenerate, unstable)
#   top_p=0.3 -> "Whispering Pines Café" x3 (truly deterministic)
#   top_p=0.7 -> "Whispers of Dawn", "Velvet Percolation", etc. (variety appears)
#   top_p=1.0 -> mostly dominant path, occasional tail option
#
# Key insight: top_p only shows its character when the prompt has multiple
# plausible answers. With a peaky distribution (e.g. coffee-shop-name -> always
# "Brewed Awakening"), even top_p=1.0 won't produce variety.
#
# top_p vs temperature: OpenAI recommends adjusting ONE, not both. Top_p is a
# safety filter (kills weird tokens); temperature is a creativity knob (reshapes
# the whole distribution). Common production combo: top_p=0.9, temperature=0.7.
# =============================================================================

top_p_values = [0.0, 0.3, 0.7, 1.0]

prompt = "Suggest a good name for a coffee shop. Do NOT use any pun involving 'brew', 'bean', or 'grind'. Be unusual and specific. Give the name in one short sentence."

for top_p in top_p_values:
    print(f"Top-p: {top_p}")
    print("=" * 40)
    for i in range(3):
        try:
            response = client.chat.completions.create(
                model = "gpt-4o-mini",
                messages = [
                    {"role": "user", "content": prompt}
                ],
                top_p = top_p,
                max_tokens = 50,
            )
            print(response.choices[0].message.content)
        except RateLimitError as e:
            print(f"Rate limit error: {e}")
        
        except APITimeoutError as e:
            print(f"API timeout error: {e}")

        except APIConnectionError as e:
            print(f"API connection error: {e}")

        except Exception as e:
            print(f"An error occurred: {e}")
    print("\n")

# recommended is not change both temperature and top-p at the same time, as they both control randomness but in different ways.
