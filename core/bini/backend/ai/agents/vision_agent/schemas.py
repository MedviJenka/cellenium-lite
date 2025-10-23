from pydantic import BaseModel, Field


class DecisionOutputSchema(BaseModel):
    """
    Schema for the output of the decision task.
    Contains the final decision (Passed/Failed) and its justification.
    """

    timestamp: str = Field(description="Timestamp of the decision.")
    justification: str = Field(description="A detailed explanation for the final decision, based on the chain of thought.")
    decision: str = Field(description="The final decision, either 'Passed' or 'Failed'.")
