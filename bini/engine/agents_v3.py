from crewai import Agent, Task, Crew
from bini.engine.azure_config import EnvironmentConfig


config = EnvironmentConfig(
        deployment_name='MODEL',
        openai_api_version='OPENAI_API_VERSION',
        azure_endpoint='AZURE_OPENAI_ENDPOINT',
        api_key='OPENAI_API_KEY'
    )

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
    description='Write a detailed code review output based on code provided',
    expected_output='code review:',
    agent=image_vision_agent
)


# Assemble a crew
crew = Crew(
    agents=[image_vision_agent],
    tasks=[image_vision_task],
    verbose=2
)


def run_image_agent() -> dict:
    return crew.kickoff()
