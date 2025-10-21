import requests
from dataclasses import dataclass
from pydantic_settings import BaseSettings
from pydantic import BaseModel, Field, PositiveInt
from requests import Response
from settings import Logfire


log = Logfire(name='api-log')


class Settings(BaseSettings):
    BASE_URL: str = 'https://jsonplaceholder.typicode.com/posts'


Config = Settings()


class ApiSchema(BaseModel):
    user_id: PositiveInt = Field(..., description='user unique')
    id: PositiveInt = Field(..., description='')
    title: str = Field(..., description='')
    body: str = Field(..., description='')


@dataclass(frozen=True)
class ApiHandler:

    url: str = Config.BASE_URL

    def get_all_data(self) -> Response:
        response = requests.get(url=self.url).json()
        print(response)
        log.fire.info(f'retrieved {len(response)} chunks')
        return response


ApiHandler().get_all_data()


