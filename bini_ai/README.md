# Bini Image Analysis Feature

## Overview

This feature introduces an automated image analysis workflow powered by AI. It allows the system to process an image (
and optionally a sample image) based on a user-provided prompt, analyze its content, and determine if it meets the
criteria defined in the prompt. The workflow leverages Large Language Models (LLMs) and Computer Vision capabilities
through a modular agent-based architecture built with CrewAI.

The core functionality includes:

1. **Prompt Refinement:** Ensuring the user's prompt is clear and grammatically correct for optimal AI processing.
2. **Image Analysis:** Utilizing a Computer Vision agent to meticulously describe the key elements, features, text, and
   colors present in the provided image(s).
3. **Chain of Thought Reasoning (Optional):** Providing a detailed step-by-step reasoning process based on the image
   analysis and the original prompt. This helps in understanding how the final decision was reached.
4. **Decision Making:** Determining whether the analyzed image(s) fulfill the requirements outlined in the user's
   prompt.
5. **Structured Output (Optional):** Providing the analysis results in a structured JSON format for easy integration and
   consumption by other systems.

## Architecture

The image analysis workflow is implemented as a CrewAI Flow named `BiniImage`. It consists of the following steps and
agents:

* **Initial State (`InitialState`):** A Pydantic model that defines the input and intermediate data structures for the
  flow. This includes the initial prompt, image paths, analysis data, and the final result.
* **English Agent (`EnglishAgent`):** Responsible for refining the initial user prompt to ensure clarity and grammatical
  correctness. This agent is used in the `refine_prompt` step.
* **Computer Vision Agent (`ComputerVisionAgent`):** A specialized agent composed of several tasks designed for image
  analysis:
    * `determine_images`: Identifies if a single or multiple images are provided.
    * `describe_main_image`: Provides a detailed description of the main image.
    * `describe_sample_images`: Provides a detailed description of the sample image (if provided).
    * `conclusion`: Synthesizes the descriptions and relates them to the original prompt.
    * `chain_of_thought`: (If enabled) Generates a step-by-step reasoning based on the image analysis.
    * `decision`: Makes the final determination (Pass/Fail) based on the analysis and reasoning.
* **Flow Steps:**
    * **`refine_prompt` (Start):** Initiates the flow by using the `EnglishAgent` to refine the user's prompt.
    * **`decision_point` (Router):** Routes the flow based on whether the prompt is deemed valid or invalid.
    * **`on_invalid_question` (Listen):** Handles cases where the initial prompt is invalid, setting the result
      accordingly.
    * **`analyze_image` (Listen):** Executes the `ComputerVisionAgent` to analyze the provided image(s) based on the (
      potentially refined) prompt.

## Usage

The `BiniUtils` class provides a convenient way to interact with the `BiniImage` flow.

### `BiniUtils` Class

* **`__init__(chain_of_thought: Optional[bool] = True, to_json: Optional[bool] = False)`:** Initializes the `BiniUtils`
  instance.
    * `chain_of_thought`: A boolean flag to enable or disable the chain of thought reasoning in the analysis. Defaults
      to `True`.
    * `to_json`: A boolean flag to enable or disable structured JSON output for the final decision task. Defaults to
      `False`.
* **`run(prompt: str, image_path: str, sample_image: Union[str, list] = '') -> str`:** Executes the `BiniImage` flow
  with the given inputs.
    * `prompt`: The user's question or instruction regarding the image(s).
    * `image_path`: The file path or URL of the main image to be analyzed.
    * `sample_image`: An optional file path or URL of a sample image for comparison. Can be a single string or a list of
      strings.
    * Returns the raw output of the final analysis step. If `to_json` is enabled and the final task (`decision`) is
      configured for JSON output, this will be a JSON string.
* **`finalize()`:** Performs any necessary cleanup after the flow execution.

### Example Usage

```python
from qasharedinfra.infra.common.services.bini_ai.src.utils.bini_utils import BiniUtils

# Initialize BiniUtils with chain of thought and JSON output enabled
bini_analyzer = BiniUtils(chain_of_thought=True, to_json=True)

# Define the prompt and image path
prompt = "Does this image contain a cat?"
image_path = "path/to/your/image.jpg"
sample_image_path = "path/to/your/sample_image.png" # Optional

# Run the image analysis flow
result = bini_analyzer.run(prompt=prompt, image_path=image_path, sample_image=sample_image_path)

# Print the result (will be a JSON string if to_json was True)
print(result)

# Finalize the BiniUtils instance
bini_analyzer.finalize()
