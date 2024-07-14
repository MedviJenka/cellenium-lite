from typing import Optional


class PromptException(Exception):

    def __init__(self, exception: Exception, message: Optional[str] = None) -> None:
        super().__init__(f'error message: {message} | exception{[exception]}')


class BiniResponseError(Exception):
    def __init__(self, outcome: object, response: str, exception: Exception) -> None:
        super().__init__(f'outcome: {outcome} response error: {response} , error: {[exception]}')
