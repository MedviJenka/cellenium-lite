from typing import Optional, Never
from abc import ABC, abstractmethod


class Executor(ABC):

    """"
    abstract executor method for complex tools
    """

    @abstractmethod
    def execute(self, *args: Optional[any], **kwargs: Optional[any]) -> Never:
        ...
