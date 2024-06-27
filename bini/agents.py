from core.manager.reader import read_json


api_key: str = read_json(env_key='GPT_API')


MODEL = 'gpt-4o'
EMBEDDING_MODEL = 'text-embedding-3-small'

TOP_K = 5
MAX_DOCS_PER_CONTENT = 8
template = """
    please answer the [question] using only following [information]
    Information: {context}
    Question: {question}
    Final answer: 
"""
