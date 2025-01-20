import logging
from datetime import datetime
from dataclasses import dataclass
from infrastructure.data.constants import LOGS


@dataclass
class Logger:

    time: object = datetime.now()
    time_format: str = f'{time: %A | %d/%m/%Y | %X}'
    format: str = f'%(levelname)s | {time_format} | %(message)s | Function: %(funcName)s | Line: %(lineno)d'

    @property
    def level(self) -> logging:

        """"
        logger method
        :params: level ........... logging level, debug, info, etc...
                 text ............ text displayed in logger
        """
        logging.basicConfig(filename=LOGS,
                            filemode='w',
                            datefmt=self.time_format,
                            format=self.format,
                            level=logging.INFO)
        return logging
