import instructor
from openai import OpenAI
from pydantic import BaseModel, Field

client = instructor.from_openai(
    OpenAI(
        api_key="local",
        base_url="http://127.0.0.1:1234/v1",
    ),
    # Local server rejects named tool_choice (instructor's default TOOLS mode), so parse JSON from the reply text.
    mode=instructor.Mode.MD_JSON,
)

class ProductReview(BaseModel):
    product_name: str = Field(description="Name of the product")
    price: float = Field(ge=0, description="Price in USD")
    rating: float = Field(ge=0, le=5, description="Rating out of 5")
    pros: list[str] = Field(description="Positive aspects")
    cons: list[str] = Field(description="Negative aspects")
    recommendation: bool

review = client.chat.completions.create(
    model="qwen/qwen3.6-35b-a3b",
    response_model=ProductReview,
    messages=[
        {
            "role": "user",
            "content": "I bought the Sony WH-1000XM5 for $348. Amazing noise cancellation, "
                       "super comfortable for long flights. Battery lasts forever. "
                       " I'd give it 4.5/5."
        }
    ],
    max_tokens=5000,  # thinking model: reasoning tokens count toward the cap
)

print(type(review))
print(review.product_name)
print(review.price)
print(review.rating)
