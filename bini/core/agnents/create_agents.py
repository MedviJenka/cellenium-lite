from dataclasses import dataclass
from core.modules.executor import Executor
from bini.infrastructure.data import SYSTEM_PROMPT


@dataclass
class Agents(Executor):

    ui_ux_feedback = "UI/UX details about the image"
    ui_ux_pass_fail = "Passed" or "Failed"
    qa_feedback = "QA details about the image"
    qa_pass_fail = "Passed" or "Failed"

    @property
    def ui_ux_manager(self) -> dict:

        """
        Simulates the prompt call to the UI/UX Manager Agent.
        Takes an image as input and returns detailed feedback and a pass/fail result.
        """
        # Simulated response from the prompt (replace with actual prompt call logic)

        return {
            "ui_ux_feedback": self.ui_ux_feedback,
            "status": self.ui_ux_pass_fail
        }

    @property
    def qa_engineer(self) -> dict:

        """
        Simulates the prompt call to the QA Engineer Agent.
        Takes an image as input and returns detailed feedback and a pass/fail result.
        """
        # Simulated response from the prompt (replace with actual prompt call logic)

        return {
            "qa_feedback": self.qa_feedback,
            "status": self.qa_pass_fail
        }

    @property
    def combined_evaluation(self) -> str:

        """
        This function calls both the UI/UX and QA prompt functions,
        combines their feedback, and determines the overall result.
        """
        # Evaluate with both agents via prompts
        # Print individual feedback

        ui_ux_result = self.ui_ux_manager['status']
        qa_result = self.qa_engineer['status']

        # Determine overall result
        overall_result = "Passed" if ui_ux_result == "Passed" and qa_result == "Passed" else "Fail"
        print("Overall Result:", overall_result)

        return overall_result

    def execute(self) -> str:
        try:
            return f'{SYSTEM_PROMPT}*{self.combined_evaluation}'
        except Exception as e:
            raise e
