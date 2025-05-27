from typing import Optional, Union
from dataclasses import dataclass
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

    debug: Optional[bool] = True

    def __post_init__(self) -> None:
        super().__init__(type(self).__name__, Service.SourceOwner.AUTOMATION)
        self.__bini_image = BiniImage(debug=self.debug)
        self.__bini_text = BiniText(debug=self.debug)

    def run(self, prompt: str, image_path: str, sample_image: Union[str, list] = '', *, as_dict: bool = False) -> Union[str, dict]:
        self.__bini_image.kickoff(inputs={'prompt': prompt, 'image': image_path, 'sample_image': sample_image})
        return self.__get_output(self.__bini_image, as_dict)

    def run_text(self, prompt: str, *, as_dict: bool = False) -> Union[str, dict]:
        self.__bini_text.kickoff(inputs={'prompt': prompt})
        return self.__get_output(self.__bini_text, as_dict)

    @staticmethod
    def __get_output(handler: any, as_dict: bool) -> Union[str, dict]:
        result = handler.flow_to_json()
        return result if as_dict else result.get('result')

    def finalize(self) -> None:
        super().finalize()
