from dataclasses import dataclass
from langchain.agents import tool
from langchain.agents import AgentExecutor
from bini.engine.azure_config import AzureOpenAIConfig
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents.format_scratchpad.openai_tools import format_to_openai_tool_messages
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser


@dataclass
class ValidationAgent:

    config = AzureOpenAIConfig()
    llm = config.set_azure_llm

    @tool
    def validation_tool(self, result: str) -> str:
        """gets result from chat gpt and refactors it to more professional and clear answer"""
        return result

    @property
    def tools(self) -> list[callable]:
        tools_list = [self.validation_tool]
        return tools_list

    @tools.setter
    def tools(self, value: any) -> None:
        self.tools.append(value)

    def bind_tools(self):
        llm_with_tools = self.llm.bind_tools(self.tools)
        return llm_with_tools

    def set_agent(self, result: str) -> list:
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are very powerful prompt validation engineer",
                ),
                ("user", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )

        agent = (
            {
                "input": lambda x: x["input"],
                "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                    x["intermediate_steps"]
                ),
                # 'chat_history': lambda y: y['chat_history'],
            }
            | prompt
            | self.bind_tools()
            | OpenAIToolsAgentOutputParser()
        )

        agent_executor = AgentExecutor(agent=agent, tools=self.tools, verbose=True)
        return list(agent_executor.stream({"input": result}))


valid = ValidationAgent()
valid.set_agent('got 3 images')
