import os
import pytest
import requests
from dotenv import load_dotenv
from functools import cached_property
from dataclasses import dataclass
from typing import Generator, List, Dict
from pydantic import BaseModel, Field, PositiveInt
from pydantic_settings import BaseSettings
from settings import Logfire


log = Logfire(name='api-log')

load_dotenv()


class Settings(BaseSettings):
    BASE_URL: str = os.getenv('BASE_URL')


Config = Settings()


class ApiSchema(BaseModel):
    userId: PositiveInt = Field(..., description='user ID')
    id: PositiveInt = Field(..., description='record ID')
    title: str
    body: str


@dataclass(frozen=True)
class APIClient:
    base_url: str = Config.BASE_URL

    @cached_property
    def _fetch_data(self) -> List[Dict]:
        """Fetch all posts once per test run."""
        try:
            response = requests.get(self.base_url, timeout=10)
            response.raise_for_status()
            data = response.json()
            log.fire.info(f"Fetched {len(data)} records from {self.base_url}")
            return data
        except requests.RequestException as e:
            log.fire.error(f"GET failed: {e}")
            return []

    def get_data_by_id(self, item_id: int) -> Dict:
        """Return a post dict matching the given ID."""
        for record in self._fetch_data:
            if record.get("id") == item_id:
                log.fire.info(f"Record found for ID {item_id}")
                return record
        log.fire.warning(f"No record found for ID {item_id}")
        return {}

    def post_data(self, schema: ApiSchema) -> int:
        """POST a new record and return the status code."""
        try:
            response = requests.post(self.base_url, json=schema.model_dump(), timeout=10)
            log.fire.info(f"POST status: {response.status_code}")
            return response.status_code
        except requests.RequestException as e:
            log.fire.error(f"POST failed: {e}")
            return 0


# ------------------- Pytest Fixtures & Tests -------------------

@pytest.fixture(scope="function")
def api_client() -> Generator[APIClient, None, None]:
    log.fire.info("Initializing API client")
    yield APIClient()
    log.fire.info("Tearing down API client")


class TestAPI:
    @pytest.mark.parametrize("item_id", [1, 5, 10])
    def test_get_data_by_id(self, api_client: APIClient, item_id: int) -> None:
        record = api_client.get_data_by_id(item_id)
        assert record, f"No data returned for ID {item_id}"
        validated = ApiSchema(**record)
        assert validated.id == item_id

    def test_post_new_record(self, api_client: APIClient) -> None:
        payload = ApiSchema(userId=1, id=999, title="Test Title", body="Body text")
        status = api_client.post_data(payload)
        assert status == 201
