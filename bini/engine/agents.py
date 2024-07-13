import os
from crewai import Agent, Task, Process, Crew


api = os.environ.get('OPENAI_API_KEY')
agent1 = Agent(role='joke teller',
               goal='tell me a joke',
               backstory='funny',
               verbose=True,
               allow_delegation=False)

agent2 = Agent(role='joke teller',
               goal='tell me a joke',
               backstory='funny',
               verbose=True,
               allow_delegation=False)

agent3 = Agent(role='joke teller',
               goal='tell me a joke',
               backstory='funny',
               verbose=True,
               allow_delegation=False)


task1 = Task(description="""tell me a joke""",
             agent=agent1)

task2 = Task(description="""tell me a joke""",
             agent=agent2)

task3 = Task(description="""tell me a joke""",
             agent=agent3)

crew = Crew(agents=[agent1, agent2, agent3],
            tasks=[task1, task2, task3],
            verbose=2,
            process=Process.sequential)

print(crew.kickoff())