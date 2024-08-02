import logging
from datetime import datetime
from bini.infrastructure.abstract_paths import BINI_LOGS


class Logger:

    def __init__(self) -> None:
        self.time: object = datetime.now()
        self.time_format: str = f'{self.time: %A | %d/%m/%Y | %X}'
        self.format: str = f'%(levelname)s | {self.time_format} | %(message)s | Function: %(funcName)s | Line: %(lineno)d'

    @property
    def level(self) -> logging:

        logging.basicConfig(filename=BINI_LOGS,
                            filemode='a',
                            datefmt=self.time_format,
                            format=self.format,
                            level=logging.INFO)

        return logging.getLogger()
