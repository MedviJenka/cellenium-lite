import time
import json
import requests
from typing import List
from dataclasses import dataclass
from pydantic import BaseModel, HttpUrl
from pydantic_settings import BaseSettings
from settings import Logfire

log = Logfire(name='test-2')


class Settings(BaseSettings):
    URL: str = "https://jsonplaceholder.typicode.com/users"


Config = Settings()


class GeoSchema(BaseModel):
    lat: str
    lng: str


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
    email: str
    phone: str
    address: AddressSchema
    website: HttpUrl | str
    company: CompanySchema


@dataclass
class ApiManager:

    timeout: int = 10
    max_retries: int = 3
    backoff_factor: float = 0.5

    def fetch_users(self) -> List[UserSchema]:

        """Fetch and validate users with retry + backoff."""

        for attempt in range(self.max_retries):
            try:
                resp = requests.get(Config.URL, timeout=self.timeout)
                resp.raise_for_status()
                raw = resp.json()
                users = [UserSchema(**each) for each in raw]
                log.fire.info(f"Fetched {len(users)} users")
                return users
            except requests.RequestException as e:
                sleep_for = self.backoff_factor * (2 ** attempt)
                log.fire.warning(f"Request failed ({e}), retrying in {sleep_for:.1f}s")
                time.sleep(sleep_for)
        raise RuntimeError("Failed to fetch users after retries")

    @staticmethod
    def save_to_file(users: List[UserSchema], path: str = "users.json") -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump([u.model_dump() for u in users], f, indent=2)
        log.fire.info(f"Saved users to {path}")

    @staticmethod
    def summarize(users: List[UserSchema]) -> None:
        first = users[0]
        print(f"Total users: {len(users)} | First user: {first.username}")


# Example usage in a test or main flow:
mgr = ApiManager()
_users = mgr.fetch_users()
mgr.save_to_file(_users)
mgr.summarize(_users)
