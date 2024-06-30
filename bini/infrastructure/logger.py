import logging
from datetime import datetime
from dataclasses import dataclass
from core.data.constants import LOGS


@dataclass
class Logger:
    def __post_init__(self) -> None:
        self.time: object = datetime.now()
        self.time_format: str = f'{self.time: %A | %d/%m/%Y | %X}'
        self.format: str = f'%(levelname)s | {self.time_format} | %(message)s | Function: %(funcName)s | Line: %(lineno)d'

    @property
    def level(self) -> logging:

        """"
        logger method
        :params: level ........... logging level, debug, info, etc...
                 text ............ text displayed in logger
        """
        logging.basicConfig(filename=LOGS,
                            filemode='a',
                            datefmt=self.time_format,
                            format=self.format,
                            level=logging.INFO)

        return logging.getLogger()
