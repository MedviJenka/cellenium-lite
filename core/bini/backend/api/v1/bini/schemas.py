from typing import Any, Optional, Dict
from pydantic import BaseModel


class AnalysisResponse(BaseModel):
    prompt: str
    result: Any


class ChatRequest(BaseModel):
    prompt: str
    chain_of_thought: bool = False
    schema_output: Optional[Dict] = None
