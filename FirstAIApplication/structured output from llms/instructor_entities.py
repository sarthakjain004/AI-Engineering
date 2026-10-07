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

class Person(BaseModel):
    name: str
    role: str = Field(description="Their role or title")
    organization: str = Field(description="Organization they belong to")

class Organization(BaseModel):
    name: str
    industry: str
    headquarters: str = Field(description="City or country of headquarters, if mentioned")

class ArticleEntities(BaseModel):
    people: list[Person]
    organizations: list[Organization]
    key_events: list[str] = Field(description="Main events described in the article")

article = """
Sundar Pichai, CEO of Google, announced a new partnership with Samsung at
the Consumer Electronics Show in Las Vegas. The deal will integrate Google's
Gemini AI into Samsung's Galaxy S25 smartphone lineup. Samsung's head of
mobile division, TM Roh, called it "a milestone for on-device AI."
Apple, which was not involved in the deal, declined to comment.
"""

result = client.chat.completions.create(
    model="qwen/qwen3.6-35b-a3b",
    response_model=ArticleEntities,
    messages=[
        {"role": "user", "content": f"Extract all entities from this article:\n\n{article}"}
    ],
    max_tokens=5000,  # thinking model: reasoning tokens count toward the cap
)

for person in result.people:
    print(f"Person: {person.name} ({person.role} at {person.organization})")

for org in result.organizations:
    print(f"Org: {org.name} ({org.industry}, {org.headquarters})")

for event in result.key_events:
    print(f"Event: {event}")
