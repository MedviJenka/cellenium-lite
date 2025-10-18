from dataclasses import dataclass
from typing import Optional, Union
from bini_ai.src.stories.bini import BiniImage


@dataclass
class BiniUtils:

    """
    Utility class to run Bini image or text analysis flows.

    If `as_dict=True`, return the full output dictionary (including prompt, date, etc.).
    If `as_dict=False`, returns only the final result (e.g., "Passed" or "Failed").
    """

    to_json: Optional[bool] = False
    chain_of_thought: Optional[bool] = True

    def __post_init__(self) -> None:
        self.__bini_image = BiniImage(chain_of_thought=self.chain_of_thought, to_json=self.to_json)

    def run(self, prompt: str, image_path: str, sample_image: Union[str, list] = '') -> str:
        return self.__bini_image.kickoff(inputs={'prompt': prompt, 'image': image_path, 'sample_image': sample_image})
