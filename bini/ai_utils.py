from dataclasses import dataclass
from typing import Optional
from bini.bini_engine import Bini
from bini.data import PROMPT_1
from core.manager.reader import read_json


@dataclass
class AIUtils(Bini):

    api_key: str = read_json(env_key='GPT_API', json_key='key')
    max_tokens: int = 400
    model: str = "gpt-4o"
    system_prompt: str = PROMPT_1

    def validate_call_metadata_for_each_row(self,
                                            image: str,
                                            row: int,
                                            *,
                                            start_time: Optional[str] = None,
                                            answer_time: Optional[str] = None,
                                            release_time: Optional[str] = None,
                                            release_cause: Optional[str] = None,
                                            tags: Optional[str] = None,
                                            notes: Optional[str] = None,
                                            recording_type: Optional[str] = None,
                                            call_expiration: Optional[str] = None,
                                            call_wait_time: Optional[str] = None,
                                            participants: Optional[str] = None,
                                            calling_party: Optional[str] = None,
                                            user_name: Optional[str] = None,
                                            duration: Optional[str] = None,
                                            date: Optional[str] = None,
                                            direction: Optional[str] = None) -> None:
        response = self.image(
            image_path=image,
            prompt=f'1. list all rows with blue circle icons and trash can icons with white triangle inside'
                   f'2. return me detailed answer for row number: {row}')
        if user_name:
            assert user_name in response
        elif duration:
            assert duration in response
        elif date:
            assert date in response  # date example Jun 20, 2024
        elif direction:
            assert direction in response
        elif start_time:
            assert start_time in response
        elif answer_time:
            assert answer_time in response
        elif release_time:
            assert release_time in response
        elif call_wait_time:
            assert call_wait_time in response
        elif participants:
            assert participants in response
        elif calling_party:
            assert calling_party in response
        elif release_cause:
            assert release_cause in response
        elif tags:
            assert tags in response
        elif notes:
            assert notes in response
        elif recording_type:
            assert recording_type in response
        elif call_expiration:
            assert call_expiration in response
