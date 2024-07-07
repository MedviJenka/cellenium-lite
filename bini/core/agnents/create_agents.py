from dataclasses import dataclass
from core.modules.executor import Executor


@dataclass
class Agents(Executor):

    ui_ux_feedback = "UI/UX details about the image"
    ui_ux_pass_fail = "Passed" or "Failed"
    qa_feedback = "QA details about the image"
    qa_pass_fail = "Passed" or "Failed"

    @property
    def image_visualization_agent(self) -> dict:
        task_description = "Analyze the image and provide visual insights."
        print(task_description)
        return {
            "ui_ux_feedback": self.ui_ux_feedback,
            "status": self.ui_ux_pass_fail,
            "report": "Image visualization task completed."
        }

    @property
    def qa_agent(self) -> str:
        task_description = "Perform QA checks and provide feedback."
        print(task_description)
        return "QA task completed."

    @property
    def ui_agent(self) -> str:
        task_description = "Evaluate UI elements and provide feedback."
        print(task_description)
        return "UI task completed."

    def main_agent(self) -> str:
        task_description = (f"Coordinate tasks between {self.image_visualization_agent, self.qa_agent, self.ui_agent} "
                            f"and summarize results.")
        print(task_description)
        return "Main agent task completed."

    def execute(self) -> dict:
        results = {
            "image_task_result": self.image_visualization_agent,
            "qa_task_result":  self.qa_agent,
            "ui_task_result": self.ui_agent,
            "main_task_result": self.main_agent()
        }
        print(results)
        return results
