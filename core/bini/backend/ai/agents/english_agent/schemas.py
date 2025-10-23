from pydantic import Field, BaseModel


class ValidateQuestionSchema(BaseModel):
    original_prompt: str = Field(..., description="The original user prompt")
