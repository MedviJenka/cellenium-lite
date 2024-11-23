from bini.core.agents.agents import CustomAgent
from bini.engine.azure_config import AzureOpenAIConfig
from bini.engine.utils import BiniUtils
from core.modules.decorators import negative


bini = BiniUtils()

azure_config = AzureOpenAIConfig()
agent = CustomAgent(config=azure_config)
print(agent.prompt_expert_agent)
print(agent.final_result_agent)

