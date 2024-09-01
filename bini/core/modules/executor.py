from typing import Optional, Never
from abc import ABC, abstractmethod


class Executor(ABC):

    """Abstract class for complex executions"""

    @abstractmethod
    def execute(self, *args: Optional[any], **kwargs: Optional[any]) -> Never:
        ...
