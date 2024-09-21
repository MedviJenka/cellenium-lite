from crewai import Agent, Task, Process, Crew
from langchain_groq import ChatGroq
from langchain.agents import Tool
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory, ReadOnlySharedMemory
from langchain.prompts import PromptTemplate
from bini.core.modules.environment import get_dotenv_data
from bini.infrastructure.prompts import Prompts


GROQ_API = get_dotenv_data('GROQ_API')
MODEL = get_dotenv_data('MODEL')
llm = ChatGroq(temperature=0, groq_api_key=GROQ_API, name_model=MODEL)

template = """
    you will rely on chat history: {chat_history} 
    you will get an input from other agent: {input}
"""

prompt = PromptTemplate(input_variables=['input', 'chat_history'], template=template)
memory = ConversationBufferMemory(memory_key='chat_history')
readonly_memory = ReadOnlySharedMemory(memory=memory)
summary_chain = LLMChain(llm=llm, prompt=prompt, verbose=True, memory=readonly_memory)


tool = [Tool(name='Summary',
             func=summary_chain.run,
             description='you will review and summarize the output from another agent')]


validation_agent = Agent(role=Prompts.validation_agent,
                         goal="validate {input} in a professional manner",
                         backstory="You're a professional prompt validation engineer",
                         verbose=True,
                         allow_delegation=False,
                         llm=llm,
                         tools=tool)

task = Task(description=Prompts.validation_agent, agent=validation_agent)
set_crew = Crew(agents=[validation_agent], tasks=[task], verbose=True, process=Process.sequential)
crew = set_crew.kickoff()

print(crew)
