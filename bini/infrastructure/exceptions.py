from abc import ABC
from typing import Optional


class BiniException(Exception, ABC):
    def __init__(self, *args: any, **kwargs: any):
        super().__init__(*args, **kwargs)


class BiniPromptException(BiniException):

    def __init__(self, exception: Exception, message: Optional[str] = None) -> None:
        super().__init__(f'error message: {message} | exception{[exception]}')
