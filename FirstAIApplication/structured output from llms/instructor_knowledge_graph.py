import instructor
from pydantic import BaseModel, Field
from openai import OpenAI

client = instructor.from_openai(
    OpenAI(
        api_key="local",
        base_url="http://127.0.0.1:1234/v1",
    ),
    # Local server rejects named tool_choice (instructor's default TOOLS mode), so parse JSON from the reply text.
    mode=instructor.Mode.MD_JSON,
)

class Entity(BaseModel):
    name: str
    entity_type: str = Field(description="person, organization, product, or event")

class Relationship(BaseModel):
    subject: str = Field(description="Name of the first entity")
    predicate: str = Field(description="Nature of the relationship (e.g., 'CEO of', 'partnered with')")
    object: str = Field(description="Name of the second entity")

class KnowledgeGraph(BaseModel):
    entities: list[Entity]
    relationships: list[Relationship]

article = """
Sundar Pichai, CEO of Google, announced a new partnership with Samsung at
the Consumer Electronics Show in Las Vegas. The deal will integrate Google's
Gemini AI into Samsung's Galaxy S25 smartphone lineup. Samsung's head of
mobile division, TM Roh, called it "a milestone for on-device AI."
Apple, which was not involved in the deal, declined to comment.
"""

graph = client.chat.completions.create(
    model="qwen/qwen3.6-35b-a3b",
    response_model=KnowledgeGraph,
    messages=[
        {"role": "user", "content": f"Extract entities and relationships:\n\n{article}"}
    ],
    max_tokens=5000,  # thinking model: reasoning tokens count toward the cap
)

for rel in graph.relationships:
    print(f"{rel.subject} --[{rel.predicate}]--> {rel.object}")
