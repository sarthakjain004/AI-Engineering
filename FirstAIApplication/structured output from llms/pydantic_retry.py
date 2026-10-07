import json
from openai import OpenAI
from pydantic import BaseModel, Field, ValidationError

client = OpenAI(
    api_key="local",
    base_url="http://127.0.0.1:1234/v1",
)

class MovieReview(BaseModel):
    title: str
    year: int = Field(ge=1888, le=2030)
    genre: list[str]
    rating: float = Field(ge=0, le=10)
    summary: str = Field(max_length=200)

def extract_with_retry(text: str, max_retries: int = 3) -> MovieReview:
    messages = [
        {
            "role": "system",
            "content": (
                "Extract movie review data and return ONLY valid JSON, no other text, "
                "with fields: "
                "title (str), year (int, 1888-2030), genre (list of str), "
                "rating (float, 0-10), summary (str, max 200 chars)."
            )
        },
        {"role": "user", "content": text},
    ]

    for attempt in range(max_retries):
        # Local server rejects response_format json_object, so JSON is requested in the prompt instead.
        response = client.chat.completions.create(
            model="qwen/qwen3.6-35b-a3b",
            messages=messages,
            max_tokens=2000,  # thinking model: reasoning tokens count toward the cap
        )

        raw_json = response.choices[0].message.content or ""

        try:
            data = json.loads(raw_json)
            review = MovieReview(**data)
            return review
        except (json.JSONDecodeError, ValidationError) as error:
            if attempt == max_retries - 1:
                raise

            error_msg = str(error)
            messages.append({"role": "assistant", "content": raw_json})
            messages.append({
                "role": "user",
                "content": f"That output had validation errors:\n{error_msg}\n\n"
                           f"Return corrected JSON only."
            })
            print(f"Attempt {attempt + 1} failed: {error_msg[:100]}...")

# Usage
review = extract_with_retry(
    "Just watched Inception (2010). Nolan's best work. A mind-bending sci-fi "
    "thriller about dreams within dreams. Solid 8.5 out of 10."
)
print(review.model_dump_json(indent=2))
