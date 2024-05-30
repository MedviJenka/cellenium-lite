import os
import json
from configparser import ConfigParser
from infrastructure.core.executor import Executor
from infrastructure.core.logger import Logger
from infrastructure.data.contants import CONFIG


log = Logger()


class GenerateDockerComposeBuild(Executor):

    def __init__(self) -> None:
        self.config = ConfigParser()

    @property
    def get_config(self) -> str:
        self.config.read(CONFIG)
        json_file_path = self.config.get('API', 'API_KEY')
        return json_file_path

    @property
    def get_json(self) -> dict:
        with open(self.get_config, 'r') as f:
            data = json.load(f)
            return data

    def execute(self) -> None:
        try:
            os.environ['API_KEY'] = self.get_json['private_key']
            log.level.info('SUCCESS: api key generated into env')
        except Exception as e:
            log.level.error(e)
            raise e


docker = GenerateDockerComposeBuild()
if __name__ == '__main__':
    docker.execute()
