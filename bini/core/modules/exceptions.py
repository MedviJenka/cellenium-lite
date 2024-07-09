from typing import Optional


class PromptException(Exception):

    def __init__(self, exception: Exception, message: Optional[str] = None) -> None:
        super().__init__(f'error message: {message} | exception{[exception]}')
