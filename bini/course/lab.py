import openai, os, requests
from core.manager.reader import read_json


openai.api_type = "azure"
openai.api_version = "2023-10-01-preview" # Version
# Azure OpenAI setup
openai.api_base = "https://openaiforaudc.openai.azure.com/" # Add your endpoint here
openai.api_key = read_json(env_key='GPT_API', json_key='key') #os.getenv("OPENAI_API_KEY")
deployment_id = 'gpt-4o-automation' # Add your deployment ID here
# Azure AI Search setup
search_endpoint = "https://openaiforaudc.openai.azure.com" # Add your Azure AI Search endpoint here
search_key = os.getenv("SEARCH_KEY") # Add your Azure AI Search admin key here
search_index_name = "search_indexer_name" # Add your Azure AI Search index name here


def setup_byod(deployment_id: str) -> None:
    """Sets up the OpenAI Python SDK to use your own data for the chat endpoint.
    :param deployment_id: The deployment ID for the model to use with your own data.
    To remove this configuration, simply set openai.requestssession to None.
    """
    class BringYourOwnDataAdapter(requests.adapters.HTTPAdapter):
        def send(self, request, **kwargs):
            request.url = f"{openai.api_base}/openai/deployments/{deployment_id}/extensions/chat/completions?api-version={openai.api_version}"
            return super().send(request, **kwargs)
    session = requests.Session()
    # Mount a custom adapter which will use the extensions endpoint for any call using the given `deployment_id`
    session.mount(
        prefix=f"{openai.api_base}/openai/deployments/{deployment_id}",
        adapter=BringYourOwnDataAdapter()
    )
    openai.requestssession = session


setup_byod(deployment_id)
message_text = [{"role": "user", "content": "What are the differences between Azure Machine Learning and Azure AI services?"}]

completion = openai.ChatCompletion.create(
    messages=message_text,
    deployment_id=deployment_id,
    dataSources=[
      {
      "type": "AzureCognitiveSearch",
      "parameters": {
        "endpoint": search_endpoint,
        "index_name": search_index_name,
        "semantic_configuration": "default",
        "query_type": "vectorSemanticHybrid",
        "fields_mapping": {},
        "in_scope": True,
        "role_information": "You are an AI assistant that helps people find information.",
        "filter": None,
        "strictness": 3,
        "top_n_documents": 5,
        "authentication": {
          "type": "api_key",
          "key": search_key
        },
        "embedding_dependency": {
          "type": "deployment_name",
          "deployment_name": "your_AI_indexer_name" # Your indexer name here
        },
        "key": search_key,
        "indexName": search_index_name
      }
    }],
    temperature=0,
    top_p=1,
    max_tokens=800,
    stop=[],
    stream=False
)
print(completion)
