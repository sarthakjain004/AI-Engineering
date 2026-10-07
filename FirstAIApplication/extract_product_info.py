import json
from openai import OpenAI

# Use local model server at http://127.0.0.1:1234
client = OpenAI(
    api_key="local",
    base_url="http://127.0.0.1:1234/v1",
)

response = client.chat.completions.create(
    model="qwen/qwen3.6-35b-a3b",
    messages=[
        {
            "role": "system",
            "content": "Extract product information from the review and return ONLY valid JSON "
                       "with fields: product_name, price, rating, pros (array), cons (array). "
                       "No other text."
        },
        {
            "role": "user",
            "content": "I bought the Sony WH-1000XM5 for a mere three hundred dollars. Amazing noise cancellation, "
                       "super comfortable for long flights. Battery lasts forever. "
                       "Only downside is the carrying case feels cheap but i think im fine with it maybe, not sure. I'd give it 4.5/5."
        }
    ],
    max_tokens=2000,  # thinking model: reasoning tokens count toward the cap
)

content = response.choices[0].message.content
print("Raw response:")
print(repr(content))
print()

if content and content.strip():
    try:
        data = json.loads(content)
        print("Parsed JSON:")
        print(json.dumps(data, indent=2))
    except json.JSONDecodeError as e:
        print(f"JSON parsing failed: {e}")
        print("Response text:")
        print(content)
else:
    print("ERROR: Empty response from model")
