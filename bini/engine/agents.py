from crewai import Task, Crew
from bini.core.modules.environment import get_secured_data
from crewai import Agent
from langchain_openai import AzureChatOpenAI
from crewai_tools import (DirectoryReadTool,
                          FileReadTool,
                          SerperDevTool,
                          WebsiteSearchTool)


azure_llm = AzureChatOpenAI(
    deployment_name=get_secured_data('MODEL'),
    openai_api_version=get_secured_data('OPENAI_API_VERSION'),
    azure_endpoint=get_secured_data('AZURE_OPENAI_ENDPOINT'),
    api_key=get_secured_data('OPENAI_API_KEY')
)
azure_agent = Agent(
    role='Example Agent',
    goal='Demonstrate custom LLM configuration',
    backstory='A diligent explorer of GitHub docs.',
    llm=azure_llm
)


docs_tool = DirectoryReadTool(directory='./blog-posts')
file_tool = FileReadTool()
search_tool = SerperDevTool()
web_rag_tool = WebsiteSearchTool()


# Define tasks
research = Task(
    description='Research the latest trends in the AI industry and provide a summary.',
    expected_output='A summary of the top 3 trending developments in the AI industry with a unique perspective on their significance.',
    agent=azure_agent
)

write = Task(
    description='Write an engaging blog post about the AI industry, based on the research analyst’s summary. Draw inspiration from the latest blog posts in the directory.',
    expected_output='A 4-paragraph blog post formatted in markdown with engaging, informative, and accessible content, avoiding complex jargon.',
    agent=azure_agent,
    output_file='blog-posts/new_post.md'  # The final blog post will be saved here
)

# Assemble a crew
crew = Crew(
    agents=[azure_agent],
    tasks=[research, write],
    verbose=2
)

# Execute tasks
crew.kickoff()
