import json
from openai import OpenAI

client = OpenAI(
    api_key="local",
    base_url="http://127.0.0.1:1234/v1",
)

response = client.chat.completions.create(
    model="qwen/qwen3.6-35b-a3b",
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "product_review",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "product_name": {"type": "string"},
                    "price": {"type": "number"},
                    "rating": {"type": "number"},
                    "pros": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "cons": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "recommendation": {"type": "boolean"}
                },
                "required": ["product_name", "price", "rating", "pros", "cons", "recommendation"],
                "additionalProperties": False
            }
        }
    },
    messages=[
        {
            "role": "system",
            "content": "Extract product information from the review."
        },
        {
            "role": "user",
            "content": "I bought the Sony WH-1000XM5 for $348. Amazing noise cancellation, "
                       "super comfortable for long flights. Battery lasts forever. "
                       "Only downside is the carrying case feels cheap. I'd give it 4.5/5."
        }
    ],
    max_tokens=2000,  # thinking model: reasoning tokens count toward the cap
)

message = response.choices[0].message
# With json_schema, this local server can put the JSON in reasoning_content and leave content empty.
text = message.content or getattr(message, "reasoning_content", None) or ""
data = json.loads(text)
print(json.dumps(data, indent=2))
