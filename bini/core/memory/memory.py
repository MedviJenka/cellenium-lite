from typing import Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage
from crewai.memory.long_term.long_term_memory_item import LongTermMemoryItem
from crewai_tools.tools.file_read_tool.file_read_tool import FileReadTool


class Memory(ABC):

    @abstractmethod
    def set_memory(self, *args: Optional[any], **kwargs: Optional[any]) -> None:
        ...


@dataclass
class MemoryEngine:

    file: str = 'memory_db.txt'

    @property
    def memory_tool(self) -> FileReadTool:
        return FileReadTool(file_path=self.file)


@dataclass
class LongTermMemory(Memory):

    def __init__(self) -> None:
        self.storage = LTMSQLiteStorage()
        super().__init__(self.storage)

    def set_memory(self, memory: LongTermMemoryItem) -> None:
        metadata = memory.metadata
        metadata.update({
            'agent': memory.agent,
            'expected_output': memory.expected_output
        })
        self.storage.save(
            task_description=memory.task,
            score=metadata['quality'],
            metadata=metadata,
            datetime=memory.datetime
        )
