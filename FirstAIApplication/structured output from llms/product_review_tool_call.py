import json
from openai import OpenAI

client = OpenAI(
    api_key="local",
    base_url="http://127.0.0.1:1234/v1",
)

response = client.chat.completions.create(
    model="qwen/qwen3.6-35b-a3b",
    tools=[
        {
            "type": "function",
            "function": {
                "name": "extract_product_review",
                "description": "Extract structured product review information from text.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "product_name": {
                            "type": "string",
                            "description": "The name of the product"
                        },
                        "price": {
                            "type": "number",
                            "description": "Price in USD"
                        },
                        "rating": {
                            "type": "number",
                            "description": "Rating out of 5"
                        },
                        "pros": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of positive points"
                        },
                        "cons": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of negative points"
                        }
                    },
                    "required": ["product_name", "price", "rating", "pros", "cons"]
                }
            }
        }
    ],
    tool_choice="required",  # local server doesn't support naming a function; one tool, so same effect
    messages=[
        {
            "role": "user",
            "content": "Extract the product info: I bought the Sony WH-1000XM5 for $348. "
                       "Amazing noise cancellation, super comfortable for long flights. "
                       "Battery lasts forever. Only downside is the carrying case feels cheap. "
                       "I'd give it 4.5/5."
        }
    ],
    max_tokens=2000,  # thinking model: reasoning tokens count toward the cap
)

tool_call = response.choices[0].message.tool_calls[0]
data = json.loads(tool_call.function.arguments)
print(json.dumps(data, indent=2))
