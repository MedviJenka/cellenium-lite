import logging
from dataclasses import dataclass
from infrastructure.data.constants import LOGS


@dataclass
class Logger:
    path: str = LOGS

    def __post_init__(self):
        self.format = '%(levelname)s | %(asctime)s | %(name)s | %(message)s | Function: %(funcName)s | Line: %(lineno)d'
        self.date = '%A | %d/%m/%Y | %X'
        self._configure_logger()

    def _configure_logger(self):
        """Configures the root logger."""
        logging.basicConfig(
            filename=self.path,
            filemode='w',
            format=self.format,
            datefmt=self.date,
            level=logging.DEBUG  # Set to DEBUG to capture all logs
        )

        # Ensure all loggers propagate to the root logger
        logging.getLogger().setLevel(logging.DEBUG)

    @staticmethod
    def log_info(message: str):
        """Logs an info message."""
        logging.info(message)

    @staticmethod
    def log_debug(message: str):
        """Logs a debug message."""
        logging.debug(message)

    @staticmethod
    def log_warning(message: str):
        """Logs a warning message."""
        logging.warning(message)

    @staticmethod
    def log_error(message: str):
        """Logs an error message."""
        logging.error(message)
