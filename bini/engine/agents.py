import os
from crewai import Agent, Task, Process, Crew


api = os.getenv('AZURE_OPENAPI_API')


agent1 = Agent(role='', goal='')
agent2 = Agent()
agent3 = Agent()
