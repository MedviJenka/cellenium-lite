from crewai import Agent, Task, Crew
from bini.engine.azure_config import EnvironmentConfig


data = {
    'deployment_name': 'MODEL',
    'openai_api_version': 'OPENAI_API_VERSION',
    'azure_endpoint': 'AZURE_OPENAI_ENDPOINT',
    'api_key': 'OPENAI_API_KEY'
}

config = EnvironmentConfig(**data)

# Create agents
image_vision_agent = Agent(
    role='UI Engineer',
    goal='Provide detailed text based on image provided',
    backstory='An expert in software testing and test plan document writing.',
    llm=config.azure_llm,
    verbose=True
)

# Define tasks
image_vision_task = Task(
    description='you will get an output from {image_vision_agent}, validate the data contains Passed value',
    expected_output='Passed',
    agent=image_vision_agent
)


# Assemble a crew
crew = Crew(
    agents=[image_vision_agent],
    tasks=[image_vision_task],
    verbose=2
)


crew.kickoff()
