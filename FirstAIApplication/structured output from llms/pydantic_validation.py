from pydantic import BaseModel, Field
from typing import Optional

class ProductReview(BaseModel):
    product_name: str = Field(description="Name of the product")
    price: float = Field(ge=0, description="Price in USD")
    rating: float = Field(ge=0, le=5, description="Rating out of 5")
    pros: list[str] = Field(description="Positive aspects")
    cons: list[str] = Field(description="Negative aspects")
    recommendation: bool = Field(description="Whether the reviewer recommends the product")
    reviewer_name: Optional[str] = Field(default=None, description="Name of the reviewer if mentioned")

valid_data = {
    "product_name": "Sony WH-1000XM5",
    "price": 348.0,
    "rating": 4.5,
    "pros": ["Great noise cancellation", "Comfortable"],
    "cons": ["Expensive case"],
    "recommendation": True,
}
review = ProductReview(**valid_data)
print(review.model_dump_json(indent=2))

try:
    bad_data = {
        "product_name": "Sony WH-1000XM5",
        "price": -50,
        "rating": 11,
        "pros": "good",
        "cons": [],
        "recommendation": True,
    }
    ProductReview(**bad_data)
except Exception as error:
    print(f"Validation error: {error}")
