import json
from asyncio import sleep

import requests
from settings import Logfire
from dataclasses import dataclass
from pydantic import BaseModel, Field
from functools import cached_property
from pydantic_settings import BaseSettings


log = Logfire(name='test')


class Config(BaseSettings):
    URL: str = 'https://jsonplaceholder.typicode.com'


Config = Config()


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


@dataclass
class ApiManager:

    retries: int = 3
    timeout: int = 10  # seconds
    endpoint: str = '/users'

    @cached_property
    def fetch_data(self) -> list[UserSchema]:

        for each_attempt in range(self.retries):

            try:
                response = requests.get(url=f'{Config.URL}{self.endpoint}', timeout=self.timeout)
                response.raise_for_status()
                raw_json = response.json()
                response_model = [UserSchema(**each_user) for each_user in raw_json]
                log.fire.info(f'{len(response_model)} users were found')
                return response_model

            except requests.HTTPError as e:
                log.fire.error(f'{e}')
                if each_attempt < self.retries:
                    each_attempt += 1
                    sleep(3)
                raise

        log.fire.error('time out')
        raise TimeoutError

    @staticmethod
    def save_json(schema: list[UserSchema], path: str = 'data.json') -> None:
        with open(path, 'w', encoding='utf-8') as file:
            json.dump([users.model_dump() for users in schema], file, indent=2)
        log.fire.info(f'json file save in: {path}')

    @staticmethod
    def summarize(schema: list[UserSchema]) -> None:
        log.fire.info(f'first username is: {schema[0].username}')


if __name__ == '__main__':
    api = ApiManager()
    api.save_json(schema=api.fetch_data)
    api.summarize(schema=api.fetch_data)
