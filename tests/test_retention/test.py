import pytest
from pydantic import Field
from dotenv import load_dotenv
from pymongo import MongoClient
from pydantic import computed_field
from functools import cached_property
from pydantic_settings import BaseSettings
from pymongo.synchronous.database import Database


load_dotenv("mongo.env")


class MongoConfig(BaseSettings):

    mongo_user: str = Field(default=..., description="mongo username ")
    mongo_password: str = Field(default=..., description="mongo password")
    mongo_host: str = Field(default=..., description="mongo host")
    mongo_cluster: str = Field(default=..., description="mongo cluster")
    mongo_app_name: str = Field(default=..., description="mongo app name")

    @computed_field
    @cached_property
    def connection_string(self) -> str:
        return f"mongodb+srv://{self.mongo_user}:{self.mongo_password}@{self.mongo_cluster}.{self.mongo_host}/?retryWrites=true&w=majority&appName={self.mongo_app_name}"


class MongoDBUtils:

    def __init__(self, database: str, config: MongoConfig) -> None:

        self.database = database
        self.__client = MongoClient(config.connection_string)
        self.__db = self.__client[self.database]

    @cached_property
    def client(self) -> MongoClient:
        """client initialization"""
        return self.__client

    @cached_property
    def db(self) -> Database:
        """main property for mongo db access"""
        return self.__db


@pytest.fixture(scope='module')
def db(database: str) -> MongoDBUtils:
    """Fixture to provide a MongoDBUtils instance for testing."""
    config = MongoConfig()
    return MongoDBUtils(database=database, config=config)


class TestRetention(MongoDBUtils):

    """
    TODO:
        ** retention period **
        scenario 1. navigate to user profile and set retention from default to 2 years
        validate in DB: user settings -> user profile -> user -> retention -> period changed to 730
        scenario 2. ui -> check extend flag -> (as above) -> period changed extend flag set to true & validate datetime in last sync
        scenario 3. ui -> check media / ai / transcription -> (as above) -> period changed extend flag set to false
        scenario 4. ui -> list view -> choose meeting -> click on ...  -> (not implement yet) -> DB -> validate meeting retention
        scenario 5. teams call -> side panel -> extend  -> (not implement yet) -> DB -> validate meeting retention
        ---
        ** zero retention period **
        scenario 1. zero retention media period -> validate with bini that media is deleted and only audio left

        "aisquad01-pri.hpbna7.mongodb.net
        5bc8f4b0-9734-4b95-a197-ae14a4e3d872
        userSettings
    """

    @pytest.mark.parametrize("db", [{"database": "5bc8f4b0-9734-4b95-a197-ae14a4e3d872"}])
    def test_connection(self, db) -> list[str]:
        mongo = MongoDBUtils(database=db, config=MongoConfig())
        return mongo.db.list_collection_names()
