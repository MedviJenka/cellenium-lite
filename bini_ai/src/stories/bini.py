from typing import Union, Optional, Type
from crewai.flow import Flow, start, listen, router
from pydantic import BaseModel, Field
from bini_ai.src.agents.english_agent.crew import EnglishAgent
from bini_ai.src.agents.vision_agent.crew import ComputerVisionAgent


class InitialState(BaseModel):
    """
    1. the flow starts with initial question aka prompt
    2. image and an optional sample image should be passed
    3. data stores all the results and passes from crew to crew
    4. the result is the final answer that is passed / failed
    5. cache is used to store all the results in a valid JSON file
    """

    prompt: str = ''
    refined_prompt: str = ''
    image: str = ''
    sample_image: Union[str, list, None] = ''
    data: str = ''
    result: str = ''
    cache: dict = Field(default_factory=dict)
    chain_of_thought: Optional[bool] = True
    output_schema: Optional[Type[BaseModel]] = None


class BiniImage(Flow[InitialState]):
    """
    BiniOps is a class that defines a flow for processing an image and a prompt.
    1. refines the prompt using an English professor agent.
    2. analyze the image using a computer vision agent.
    3. think through the data using a chain of thought agent.
    4. decides the final result based on the validation.

    """

    @start()
    def refine_prompt(self) -> None:
        agent = EnglishAgent(chain_of_thought=self.state.chain_of_thought)
        """getting the original prompt and refines to correct english"""
        self.state.prompt = agent.execute(prompt=self.state.prompt)

    # ----------------------------------------------------------------------------------------------------------------------

    @router(refine_prompt)
    def decision_point(self) -> str:
        if self.state.prompt == 'Invalid Question':
            return 'Invalid Question'
        return 'Valid Question'

    # ----------------------------------------------------------------------------------------------------------------------

    @listen('Invalid Question')
    def on_invalid_question(self) -> str:
        return 'Invalid Question'

    @listen('Valid Question')
    def analyze_image(self) -> str:
        """analyzes the image using AI"""
        agent = ComputerVisionAgent(chain_of_thought=self.state.chain_of_thought, output_schema=self.state.output_schema)
        return agent.execute(prompt=self.state.prompt,
                             image_path=self.state.image,
                             sample_image=self.state.sample_image)


BiniImage().kickoff(inputs={'chain_of_thought': True})
