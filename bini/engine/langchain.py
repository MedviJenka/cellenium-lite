import os
import json
from dataclasses import dataclass
from openai import AzureOpenAI
from bini.core.data.constants import API_KEY


@dataclass
class AgentEngine:

    api_key: str
    api_version: str
    endpoint: str
    model: str
    client: AzureOpenAI = None
    assistant: any = None
    thread: any = None
    run: any = None

    def __post_init__(self):
        self.client = AzureOpenAI(
            api_key=self.api_key,
            api_version=self.api_version,
            azure_endpoint=self.endpoint
        )

    def call_agent(self, instructions: str, model: str):
        self.assistant = self.client.beta.assistants.create(
            instructions=instructions,
            model=model,
            tools=[]
        )

    def create_thread(self):
        self.thread = self.client.beta.threads.create()

    def add_user_message(self, content: str):
        self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=content
        )

    def run_thread(self):
        self.run = self.client.beta.threads.runs.create(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id
        )

        while self.run.status in ['queued', 'in_progress', 'cancelling']:
            self.run = self.client.beta.threads.runs.retrieve(
                thread_id=self.thread.id,
                run_id=self.run.id
            )

        if self.run.status == 'completed':
            messages = self.client.beta.threads.messages.list(
                thread_id=self.thread.id
            )
            return messages
        elif self.run.status == 'requires_action':
            pass
        else:
            print(self.run.status)


class CreateAgent:

    def __init__(self):
        self.client = AgentEngine(
            api_key=API_KEY,
            api_version="2024-02-15-preview",
            endpoint='https://openaigpt4audc.openai.azure.com',
            model='bini'
        )

    @staticmethod
    def get_agent_roles() -> any:
        with open('agent_roles.json', 'r') as agents:
            return json.load(agents)

    def run_agent_workflow(self, system_instructions: str, user_message: str):
        self.client.call_agent(
            instructions=system_instructions,
            model=self.client.model
        )
        self.client.create_thread()
        self.client.add_user_message(user_message)
        messages = self.client.run_thread().data

        for message in messages:
            if message.role == 'assistant':
                for content_block in message.content:
                    if hasattr(content_block, 'text') and hasattr(content_block.text, 'value'):
                        return content_block.text.value


class GenerateAgents(CreateAgent):

    def image_agent(self):
        return self.run_agent_workflow(system_instructions=self.get_agent_roles()[0]['type'],
                                       user_message=self.get_agent_roles()[1]['prompt'])

    def qa_agent(self):
        return self.run_agent_workflow(system_instructions=self.get_agent_roles()[1]['type'],
                                       user_message=self.get_agent_roles()[1]['prompt'])

    def ui_agent(self):
        return self.run_agent_workflow(system_instructions=self.get_agent_roles()[2]['type'],
                                       user_message=self.get_agent_roles()[1]['prompt'])


agent = GenerateAgents()
if __name__ == '__main__':
    print(agent.image_agent())
