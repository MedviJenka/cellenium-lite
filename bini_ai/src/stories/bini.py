import os
import uuid
import json
from typing import Union, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from crewai.flow import Flow, start, listen, router
from qasharedinfra.infra.common.services.bini_ai.infrastructure.project_path import GLOBAL_PATH
from qasharedinfra.infra.common.services.bini_ai.src.agents.english_agent.crew import EnglishAgent
from qasharedinfra.infra.common.services.bini_ai.src.agents.validation_agent.crew import ValidationAgent
from qasharedinfra.infra.common.services.bini_ai.src.agents.vision_agent.crew import ComputerVisionAgent


class InitialState(BaseModel):

    """
    1. the flow starts with initial question aka prompt
    2. image and an optional sample image should be passed
    3. data stores all the results and passes from crew to crew
    4. the result is the final answer that is passed / failed
    5. cache is used to store all the results in a valid JSON file
    """

    prompt: str = ''
    image: str = ''
    sample_image: Union[str, list, None] = ''
    data: str = ''
    result: str = ''
    cache: dict = Field(default_factory=dict)
    retries: int = 0


class BiniImage(Flow[InitialState]):

    """
    BiniOps is a class that defines a flow for processing an image and a prompt.
    1. refines the prompt using an English professor agent.
    2. analyze the image using a computer vision agent.
    3. think through the data using a chain of thought agent.
    4. decides the final result based on the validation.

    """

    def __init__(self, debug: Optional[bool] = False) -> None:
        super().__init__()
        self.debug = debug
        self.english_agent = EnglishAgent(debug=self.debug)
        self.computer_vision_agent = ComputerVisionAgent(debug=self.debug)
        self.validation_agent = ValidationAgent(debug=self.debug)

    @start()
    def refine_prompt(self) -> None:
        """getting the original prompt and refines to correct english"""
        self.state.cache['date'] = datetime.now().strftime("%d/%m/%Y at %H:%M")
        self.state.prompt = self.english_agent.execute(prompt=self.state.prompt)
        self.state.cache['refined_prompt'] = self.state.prompt

# ----------------------------------------------------------------------------------------------------------------------

    @router(refine_prompt)
    def decision_point_1(self) -> str:
        if self.state.prompt == 'Invalid Question':
            return 'Invalid Question'
        return 'Valid Question'

# ----------------------------------------------------------------------------------------------------------------------

    @listen('Invalid Question')
    def on_invalid_question(self) -> None:
        self.state.result = 'Invalid'
        self.state.cache['result'] = 'Invalid Question'
        return

    @listen('Valid Question')
    def analyze_image(self) -> None:
        """analyzes the image using AI"""
        self.state.data = self.computer_vision_agent.execute(prompt=self.state.prompt,
                                                             image_path=self.state.image,
                                                             sample_image=self.state.sample_image)
        self.state.cache['image_data'] = self.state.data

    @listen(analyze_image)
    def validate_data(self) -> None:
        """validates the data using AI"""
        self.state.data = self.validation_agent.execute(original_prompt=self.state.prompt, image_data=self.state.data)
        self.state.cache['validation_data'] = self.state.data

# ----------------------------------------------------------------------------------------------------------------------

    @router(validate_data)
    def decision_point_2(self) -> str:
        """meaning: if self.state.data == 'Passed' then a result = 'Passed' else return 'Failed'"""
        if 'Passed' in self.state.data:
            self.state.result = 'Passed'
        elif 'Failed' in self.state.data:
            self.state.result = 'Failed'
        return self.state.result

# ----------------------------------------------------------------------------------------------------------------------

    @listen('Passed')
    def on_success(self) -> None:
        self.state.cache['result'] = 'Passed'

    @listen('Failed')
    def on_failure(self) -> None:
        self.state.cache['result'] = 'Failed'

    def flow_to_json(self) -> dict:

        results_dir = fr'{GLOBAL_PATH}\qasharedinfra\infra\common\services\bini_ai\results'

        if not os.path.exists(results_dir):
            os.makedirs(results_dir)

        json_path = fr'{results_dir}\bini-output.json-{uuid.uuid4()}'

        # Write the cache to JSON file
        with open(json_path, 'w') as file:
            json.dump(self.state.cache, file, indent=4)

        # Return the full cache dictionary
        return dict(self.state.cache)
