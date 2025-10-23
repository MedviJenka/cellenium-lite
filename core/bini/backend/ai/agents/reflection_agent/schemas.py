from pydantic import BaseModel


class ReflectionOutputSchema(BaseModel):
    is_response_ok: bool
    issues: str
    suggestions: str
