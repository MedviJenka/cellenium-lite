from typing import Type, List

import requests
from settings import Logfire
from dataclasses import dataclass
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


log = Logfire(name='test4')


class GeoSchema(BaseModel):
    lat: str = Field(description='latitude')
    lng: str = Field(description='longitude')


class AddressSchema(BaseModel):
    street: str
    suite: str
    city: str
    zipcode: str
    geo: GeoSchema


class CompanySchema(BaseModel):
    name: str
    catchPhrase: str
    bs: str


class UserSchema(BaseModel):
    id: int
    name: str
    username: str
    address: AddressSchema
    phone: str
    website: str
    company: CompanySchema


class PostsSchema(BaseModel):
    userId: int
    id: int
    title: str
    body: str


class Config(BaseSettings):
    USERS: str = "https://jsonplaceholder.typicode.com/users"
    POSTS: str = "https://jsonplaceholder.typicode.com/posts"
    ERROR: str = "https://httpstat.us/503"


Config = Config()


@dataclass
class APIManager:

    retries: int = 3
    timeout: int = 10

    def _fetch_data(self, url: Config, schema: Type[BaseModel]) -> list:

        for each_attempt in range(1, self.retries):
            try:
                response = requests.get(url=url, timeout=self.timeout)
                if response.status_code > 400:
                    raise requests.HTTPError
                raw = response.json()
                response_schema = [schema(**each) for each in raw]
                return response_schema

            except requests.HTTPError as e:
                log.fire.warning(f'{e}')
                raise

        log.fire.error('timeout error')
        raise TimeoutError

    def get_users(self) -> list:
        response = self._fetch_data(url=Config.USERS, schema=UserSchema)
        log.fire.info(f'{response}')
        return response

    def get_posts(self) -> list:
        response = self._fetch_data(url=Config.POSTS, schema=PostsSchema)
        log.fire.info(f'{response}')
        return response


if __name__ == '__main__':
    api = APIManager()
    api.get_users()
    api.get_posts()
