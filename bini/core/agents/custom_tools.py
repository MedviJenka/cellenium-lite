from pydantic import BaseModel, Field
from langchain.tools import tool


class BaseImageTool(BaseModel):
    operator: str = Field(..., description='')
    factor: str = Field(..., description='')


@tool("validate this image", args_schema=BaseImageTool, return_direct=True)
def perform() -> None: ...
