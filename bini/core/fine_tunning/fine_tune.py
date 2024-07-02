from docx import Document
from langchain.llms import OpenAI
from langchain.chains import TextChain


def extract_text_from_docx(path: str) -> str:
    doc = Document(path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text


file_path = 'example.docx'
text_data = extract_text_from_docx(file_path)

# Initialize the OpenAI API key
openai_api_key = "your_openai_api_key_here"

# Initialize the LLM (Language Model)
llm = OpenAI(api_key=openai_api_key)

# Create a TextChain instance with the extracted text data
text_chain = TextChain(llm=llm, input_text=text_data)

# Define a simple prompt for the chain
prompt = "Please summarize the following text:"

# Run the chain with the prompt and text data
response = text_chain.run(prompt=prompt)

# Print the response
print(response)
