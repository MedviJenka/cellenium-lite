from dataclasses import dataclass
from typing import Optional, Union

from coreinfra.core.common.service import Service
from qasharedinfra.infra.common.services.bini_ai.src.stories.bini import BiniImage
from qasharedinfra.infra.common.services.bini_ai.src.stories.text import BiniText


@dataclass
class BiniUtils(Service):
    """
    Utility class to run Bini image or text analysis flows.

    If `as_dict=True`, return the full output dictionary (including prompt, date, etc.).
    If `as_dict=False`, returns only the final result (e.g., "Passed" or "Failed").
    """

    to_json: Optional[bool] = False
    chain_of_thought: Optional[bool] = True

    def __post_init__(self) -> None:
        super().__init__(type(self).__name__, Service.SourceOwner.AUTOMATION)
        self.__bini_image = BiniImage(chain_of_thought=self.chain_of_thought, to_json=self.to_json)
        self.__bini_text = BiniText(chain_of_thought=self.chain_of_thought, to_json=self.to_json)

    def run(self, prompt: str, image_path: str, sample_image: Union[str, list] = '') -> str:
        return self.run_image(prompt=prompt, image_path=image_path, sample_image=sample_image)

    def run_image(self, prompt: str, image_path: str, sample_image: Union[str, list] = '') -> str:
        return self.__bini_image.kickoff(inputs={'prompt': prompt, 'image': image_path, 'sample_image': sample_image})

    def finalize(self) -> None:
        super().finalize()
