from typing import Union
from pydantic import BaseModel, Field


class BiniImageInitialState(BaseModel):
    """State passed between steps."""
    original_prompt:  str = Field(default='', description="The original user prompt")
    refined_prompt:   str = Field(default='', description="The refined prompt after English correction")
    cached_state:     str = Field(default='', description="Cached state or status label")
    image:            str = Field(default='', description="Path to the input image")
    sample_image:     Union[str, list, None] = Field(default=None, description="Path(s) to sample image(s)")
    result:           Union[str, dict, None] = Field(default=None, description="Final result of the analysis")
    chain_of_thought: bool = Field(default=True, description="Whether to use chain of thought reasoning")
    to_json:          bool = Field(default=True, description="Whether to format output as JSON")
    reflection:       str = Field(default='', description='Reflection or critical thinking output')
