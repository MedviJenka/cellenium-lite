from settings import Logfire
from typing import Optional, Type
from pydantic import BaseModel, Field
from crewai.flow import Flow, start
from core.bini.backend.ai.agents.chat_agent.crew import ChatAgent


log = Logfire("bini-chat-flow")


class InitialState(BaseModel):
    model_config = {'arbitrary_types_allowed': True}
    
    prompt: str = ''
    chain_of_thought: Optional[bool] = True
    cache: dict = Field(default_factory=dict)
    schema_output: Optional[Type[BaseModel]] = None


class BiniChatFlow(Flow[InitialState]):

    @start()
    def run_text_agent(self) -> dict:

        agent = ChatAgent(chain_of_thought=self.state.chain_of_thought, schema_output=self.state.schema_output)

        self.state.cache = {
            "response": agent.execute(prompt=self.state.prompt)
        }
        log.fire.info(f'{self.state.cache}')
        return self.state.cache
