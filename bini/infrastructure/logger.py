import logging
from datetime import datetime
from dataclasses import dataclass
from bini.core.data.abstract_paths import BINI_LOGS


@dataclass
class Logger:

    def __post_init__(self) -> None:
        self.time: object = datetime.now()
        self.time_format: str = f'{self.time: %A | %d/%m/%Y | %X}'
        self.format: str = f'%(levelname)s | {self.time_format} | %(message)s | Function: %(funcName)s | Line: %(lineno)d'

        logging.basicConfig(filename=BINI_LOGS,
                            filemode='a',
                            datefmt=self.time_format,
                            format=self.format,
                            level=logging.INFO)
        self.logger = logging.getLogger()

    @property
    def level(self) -> logging:
        return self.logger
