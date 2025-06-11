from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel
from crewai_tools import CodeDocsSearchTool


class FunctionMappingTool(BaseTool):

    name: str = "Function Mapping Tool"
    description: str = "getting the relevant functions"
    query: Type[BaseModel] = ...

    def _run(self, query: str) -> str: ...
