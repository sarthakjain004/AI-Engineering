import time
import random
from dotenv import load_dotenv
from openai import OpenAI, RateLimitError, APITimeoutError, APIConnectionError
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    timeout = 1,
)

def call_with_retry(client, max_retries=3, **kwargs):
    """
    Makes an LLM API call with exponential backoff retry logic.
    Retries on rate limits, timeouts, and connection errors.
    """
    for attempt in range(max_retries + 1):
        try:
            response = client.chat.completions.create(**kwargs)
            return response

        except RateLimitError as e:
            if attempt == max_retries:
                raise
            # Exponential backoff: 1s, 2s, 4s + random jitter
            wait_time = (2 ** attempt) + random.uniform(0, 1)
            print(f"Rate limited. Retrying in {wait_time:.1f}s (attempt {attempt + 1}/{max_retries})")
            time.sleep(wait_time)

        except APITimeoutError as e:
            if attempt == max_retries:
                raise
            wait_time = (2 ** attempt) + random.uniform(0, 1)
            print(f"Timeout. Retrying in {wait_time:.1f}s (attempt {attempt + 1}/{max_retries})")
            time.sleep(wait_time)

        except APIConnectionError as e:
            if attempt == max_retries:
                raise
            wait_time = (2 ** attempt) + random.uniform(0, 1)
            print(f"Connection error. Retrying in {wait_time:.1f}s (attempt {attempt + 1}/{max_retries})")
            time.sleep(wait_time)
			
response = call_with_retry(
    client,
    max_retries=3,
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": "Explain TCP vs UDP in one paragraph."}
    ]
)
print(response.choices[0].message.content)			