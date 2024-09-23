from bini.core.agents.prompt_agent import SetAgent


n_iterations = 2
inputs = {"topic": "CrewAI Training"}
crew = SetAgent()


try:
    crew.set_crew().train(n_iterations=n_iterations, inputs=inputs)

except Exception as e:
    raise Exception(f"An error occurred while training the crew: {e}")
