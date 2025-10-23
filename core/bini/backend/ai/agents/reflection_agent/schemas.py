from pydantic import BaseModel, Field


class ReflectionOutputSchema(BaseModel):
    is_response_ok: bool
    fixed_prompt: str
    chain_of_thought: str
    final_decision: str = Field(description='passed or failed')
