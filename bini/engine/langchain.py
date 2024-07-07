import time
from dataclasses import dataclass
from openai import AzureOpenAI
from bini.core.data.constants import API_KEY


@dataclass
class AgentEngine:

    api_key: str
    api_version: str
    endpoint: str
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
            time.sleep(1)
            self.run = self.client.beta.threads.runs.retrieve(
                thread_id=self.thread.id,
                run_id=self.run.id
            )

        if self.run.status == 'completed':
            messages = self.client.beta.threads.messages.list(
                thread_id=self.thread.id
            )
            print(messages)
        elif self.run.status == 'requires_action':
            # the assistant requires calling some functions
            # and submit the tool outputs back to the run
            pass
        else:
            print(self.run.status)


class CreateAgent:

    def __init__(self):
        self.client = AgentEngine(
            api_key=API_KEY,
            api_version="2024-02-15-preview",
            endpoint='https://openaigpt4audc.openai.azure.com'
        )
        self.run_agent_workflow()

    def run_agent_workflow(self):
        self.client.call_agent(
            instructions="You're a professional QA engineer, and you will validate the image that was provided to you.",
            model="bini"  # replace with model deployment name
        )
        self.client.create_thread()
        self.client.add_user_message("validate this image:")  # Replace this with your prompt
        self.client.run_thread()


# Instantiate and run the CreateAgent
agent = CreateAgent()
print(agent.run_agent_workflow())
