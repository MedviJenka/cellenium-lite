from bini.core.agents.agents import EnvironmentConfig


def test_agent_1() -> None:

    azure_llm = EnvironmentConfig(deployment_name='MODEL',
                                  openai_api_version='OPENAI_API_VERSION',
                                  azure_endpoint='AZURE_OPENAI_ENDPOINT',
                                  api_key='OPENAI_API_KEY')

    __azure = azure_llm.set_azure_llm
