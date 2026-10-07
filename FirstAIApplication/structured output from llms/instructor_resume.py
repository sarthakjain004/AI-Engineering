import instructor
from openai import OpenAI
from pydantic import BaseModel, Field, field_validator
from typing import Optional

class Experience(BaseModel):
    company: str
    title: str
    start_year: int = Field(ge=1950, le=2030)
    end_year: Optional[int] = Field(default=None, ge=1950, le=2030)
    is_current: bool = Field(default=False, description="True if this is the current role")
    highlights: list[str] = Field(description="Key achievements or responsibilities")

class Education(BaseModel):
    institution: str
    degree: str
    field_of_study: str
    graduation_year: int = Field(ge=1950, le=2030)

class ResumeData(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    summary: str = Field(description="Professional summary in 1-2 sentences")
    skills: list[str] = Field(min_length=1, description="Technical and soft skills")
    experience: list[Experience] = Field(min_length=1)
    education: list[Education]
    total_years_experience: int = Field(ge=0)

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        if v is not None and "@" not in v:
            raise ValueError("Invalid email format")
        return v

client = instructor.from_openai(
    OpenAI(
        api_key="local",
        base_url="http://127.0.0.1:1234/v1",
    ),
    # Local server rejects named tool_choice (instructor's default TOOLS mode), so parse JSON from the reply text.
    mode=instructor.Mode.MD_JSON,
)

def parse_resume(raw_text: str) -> ResumeData:
    """Parse raw resume text into a ResumeData object."""
    return client.chat.completions.create(
        model="qwen/qwen3.6-35b-a3b",
        response_model=ResumeData,
        max_retries=3,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a resume parsing assistant. Extract structured data "
                    "from the resume text provided. Be precise with dates and "
                    "job titles. If information is not present, use null for "
                    "optional fields. For total_years_experience, calculate the "
                    "approximate total from the work history."
                )
            },
            {"role": "user", "content": raw_text},
        ],
        max_tokens=20000,  # thinking model: reasoning tokens count toward the cap
    )

sample_resume = """
Jane Chen
jane.chen@email.com | (555) 123-4567 | San Francisco, CA

Senior Software Engineer with 8 years of experience in distributed systems
and cloud infrastructure.

EXPERIENCE

Senior Software Engineer, Stripe (2021 - Present)
- Led migration of payment processing pipeline to event-driven architecture
- Reduced P99 latency by 40% through caching layer redesign
- Mentored team of 4 junior engineers

Software Engineer, Dropbox (2018 - 2021)
- Built real-time file sync engine handling 50M daily operations
- Implemented conflict resolution algorithm for concurrent edits
- Owned on-call rotation for storage infrastructure

Junior Developer, Startup Inc (2016 - 2018)
- Full-stack development with Python/Django and React
- Built internal tools that saved 20 engineering hours per week

EDUCATION
BS Computer Science, UC Berkeley, 2016

SKILLS
Python, Go, Java, Kubernetes, AWS, PostgreSQL, Kafka, Redis,
Distributed Systems, System Design, Technical Leadership
"""

resume = parse_resume(sample_resume)
print(f"Name: {resume.name}")
print(f"Email: {resume.email}")
print(f"Skills: {', '.join(resume.skills[:5])}...")
print(f"Experience: {len(resume.experience)} roles")
print(f"Total years: {resume.total_years_experience}")

for exp in resume.experience:
    current = " (current)" if exp.is_current else ""
    print(f"  - {exp.title} at {exp.company}, {exp.start_year}-{exp.end_year or 'Present'}{current}")

def parse_resume_safe(raw_text: str) -> dict:
    try:
        resume = parse_resume(raw_text)
        return {"success": True, "data": resume.model_dump()}
    except Exception as error:
        return {
            "success": False,
            "error": str(error),
            "raw_text_length": len(raw_text),
        }

minimal_resume = "John Doe, Python developer, 3 years experience at Google."
result = parse_resume_safe(minimal_resume)

if result["success"]:
    print("Parsed successfully")
else:
    print(f"Failed: {result['error']}")
