# BiniOps — Multistage AI Flow for Image and Prompt Analysis

`BiniOps` is a modular flow-based AI pipeline built on the `CrewAI` framework, designed to process an input prompt and image, refine the prompt, analyze the image, reason through the results, and return a final validation outcome. The flow also maintains a full trace of its decision-making process for transparency and debugging.

---

## 🚀 Features

- **Prompt Refinement** – Uses an English Professor agent to clean and refine the input prompt.
- **Image Analysis** – Leverages a Computer Vision agent to interpret and extract data from the image.
- **Chain-of-Thought Reasoning** – Applies logical reasoning over the analyzed data.
- **Validation** – Uses a Validation Agent to confirm whether the image data meets expected criteria.
- **Flow Control** – Decision routing based on result: Passed, Failed, or Invalid.
- **Traceability** – Maintains a `cache` of all steps for full auditability.

---

## 🧠 Agents Used

| Agent               | Description                                                  |
|---------------------|--------------------------------------------------------------|
| EnglishProfessor    | Improves the clarity and structure of the input prompt.      |
| ComputerVisionAgent | Analyzes the image using computer vision capabilities.       |
| ChainOfThought      | Applies logical reasoning to the image analysis.             |
| ValidationAgent     | Validates whether the final data satisfies defined criteria. |

---

## 📥 Input Format

```json
{
  "prompt": "Describe the contents of the image",
  "image": "/path/to/image.png",
  "sample_image": "/path/to/sample.png" 
}
```

---

## 🔄 Flow Breakdown

1. **Refine Prompt**
2. **Analyze Image**
3. **Reason Through**
4. **Validate Result**
5. **Make Decision**
6. **Return Final Status** (`Passed`, `Failed`, or `Invalid`)

Each stage updates a central state object (`InitialState`) and appends to a cache for traceability.

---

## 📤 Output (flow_to_json)

Returns a JSON-formatted object like:

```json
{
  "prompt": "...refined prompt...",
  "data": "...processed data...",
  "result": "Passed",
  "cache": "[...full history...]",
  "status": "Passed"
}
```

---

## 🚰 Requirements

- Python 3.12+
- `CrewAI`
- `Pydantic`
- Custom agents from `qasharedinfra`

---

## 📌 Notes

- This module is designed to be integrated within a larger AI pipeline or service.
- All agents are assumed to be preconfigured and available via internal imports.

