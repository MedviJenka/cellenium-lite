from pydantic import BaseModel, Field


class ReflectionOutputSchema(BaseModel):
    is_response_ok: bool
    issues: str
    suggestions: str
    final_decision: str = Field(description='passed or failed')
