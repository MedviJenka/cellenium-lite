import os
import uuid
import json
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from crewai.flow import Flow, start, listen
from qasharedinfra.infra.common.services.bini_ai.src.agents.text_agent.crew import TextAgent
from qasharedinfra.infra.common.services.bini_ai.infrastructure.project_path import GLOBAL_PATH
from qasharedinfra.infra.common.services.bini_ai.src.agents.english_agent.crew import EnglishAgent


class InitialState(BaseModel):

    """
    1. the flow starts with initial question aka prompt
    2. image and an optional sample image should be passed
    3. data stores all the results and passes from crew to crew
    4. the result is the final answer that is passed / failed
    5. cache is used to store all the results in a valid JSON file
    """

    prompt: str = ''
    data: str = ''
    result: str = ''
    cache: dict = Field(default_factory=dict)


class BiniText(Flow[InitialState]):

    def __init__(self, debug: Optional[bool] = False) -> None:
        super().__init__()
        self.debug = debug
        self.english_agent = EnglishAgent(debug=self.debug)
        self.text_agent = TextAgent(debug=self.debug)

    @start()
    def refine_prompt(self) -> None:
        """getting the original prompt and refines to correct english"""
        self.state.cache['date'] = datetime.now().strftime("%d/%m/%Y at %H:%M")
        self.state.prompt = self.english_agent.execute(prompt=self.state.prompt)
        self.state.cache['refined_prompt'] = self.state.prompt

    @listen(refine_prompt)
    def run_text_agent(self) -> str:
        """running text agent"""
        self.state.data = self.text_agent.execute(prompt=self.state.prompt)
        self.state.cache['result'] = self.state.prompt
        return self.state.data

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


if __name__ == '__main__':
    bini = BiniText(debug=True)
    with open(file=r"C:\Users\evgenyp\Downloads\tenants.html", encoding='utf-8') as html_file:
        string = html_file.read()
        bini.kickoff(inputs={'prompt': f'extract data from the HTML table as json file: {string}'})
