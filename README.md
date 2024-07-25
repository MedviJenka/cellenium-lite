# Bini OpenAI Deployment Manager 
#### version: 1.0.0

This repository contains a Python module for managing interactions with the Bini OpenAI deployment. 
The module is designed to facilitate communication with the OpenAI service in Azure, 
particularly focusing on image processing and visualization tasks.

* Table of Contents
* Installation
* Usage
* Class Details
* Attributes
* Methods
* Exception Handling
* Installation

### To use this module, ensure you have the following dependencies installed:

## modules:
    pip install requests langchain lanchain-openai crewai crewai[tools] 

## openai azure credentials
1. navigate to azure portal
2. choose a model (or create one)

    ![img.png](img.png)

3. click on key and endpoint 

    ![img_1.png](img_1.png)

4. endpoint name will be set in .env file which you will create in next steps \
   .env key and value example: 
     * AZURE_OPENAI_ENDPOINT = https://openaigpt4audc.openai.azure.com
    
   ![img_2.png](img_2.png)

5. module name can be obtained through navigating to manage deployments
   .env key and value example: 
     * MODEL = bini
![img_3.png](img_3.png)
![img_4.png](img_4.png)

6. version name can be obtained 
   .env key and value example: 
     * OPENAI_API_VERSION = 2024-02-15-preview
![img_5.png](img_5.png)

7. last one is API key:
    * 

## .env file:
    1. create .env file in root dir
    2. .env keys should be exactly as env_template.env 
    3. get the data from you azure portal

## env file example:
    AZURE_OPENAI_API = 123456789
    ENDPOINT = https://openaigpt4audc.openai.azure.com
    MODEL = bini
    VERSION = 2024-02-15-preview

## code example: 
    from bini import Bini
    
    # Initialize the Bini object
    bini = Bini(
        model="your_model_name",
        api_key="your_api_key",
        version="your_api_version",
        temperature=0.7
    )
    
    # Run the Bini agent with an image and a prompt
    response = bini.run(
        image_path="path_to_your_image.jpg",
        prompt="Describe the image",
        sample_image="path_to_sample_image.jpg"
    )
    
    # Compare two images with an optional prompt
    compare_response = bini.image_compare(
        image_path="path_to_image.jpg",
        compare_to="path_to_compare_image.jpg",
        prompt="Compare these images"
    )

## Class Details

### Attributes:
    model (str): The model name for the OpenAI deployment.
    api_key (str): The API key for accessing the OpenAI service.
    version (str): The version of the OpenAI API to use.
    temperature (float): The temperature setting for the OpenAI model responses.

### Methods
    __post_init__(self) -> None: Initializes the Bini class with the correct endpoint.
    image_agent(self) -> str: Sends a request to the image agent with or without a sample image.
    run(self, image_path: str, prompt: str, sample_image: Optional[str] = '') -> str: Runs the appropriate agents based on the call_agents flag.
    image_compare(self, image_path: str, compare_to: str, prompt: Optional[str] = '') -> str: Processes an image with a given prompt using the image visualization agent.
    Exception Handling
    The run and image_compare methods handle exceptions related to file not found errors and request exceptions, raising them appropriately.
