import logfire
import warnings
from functools import cached_property
from dataclasses import dataclass, field
from backend.settings import Config


warnings.filterwarnings('ignore')


@dataclass
class Logfire:

    name: str
    _logger: logfire = field(init=False, default=None)

    @cached_property
    def fire(self):
        return logfire.configure(service_name=self.name, token=Config.LOGFIRE_TOKEN)
