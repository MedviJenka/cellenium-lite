import os
from bson import ObjectId
from pydantic import Field
from dotenv import load_dotenv
from pymongo import MongoClient
from functools import cached_property
from pydantic_settings import BaseSettings
from pymongo.collection import Collection
from pymongo.synchronous.database import Database
from typing import Literal, Optional, Dict, List


load_dotenv("mongo.env")

# devming
# DATABASE_ID = "05f68ce2-ee68-4bfc-8b6e-60e5b34d95e0"

# aisquad01

MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_CLUSTER = os.getenv("MONGO_CLUSTER")
MONGO_APP_NAME = os.getenv("MONGO_APP_NAME")


class Logger:

    def error(self, message: str) -> None:...
    def bug(self, message: str) -> None: ...
    def warning(self, message: str) -> None: ...


log = Logger()


class MongoDBConfig(BaseSettings):

    mongo_user: str = Field(default=MONGO_USER, description="mongo username")
    mongo_password: str = Field(default=MONGO_PASSWORD, description="mongo password")
    mongo_host: str = Field(default=MONGO_HOST, description="mongo host")
    mongo_cluster: str = Field(default=MONGO_CLUSTER, description="mongo cluster")
    mongo_app_name: str = Field(default=MONGO_APP_NAME, description="mongo app name")

    @property
    def connection_string(self) -> str:
        return f"mongodb+srv://{self.mongo_user}:{self.mongo_password}@{self.mongo_cluster}.{self.mongo_host}/?retryWrites=true&w=majority&appName={self.mongo_app_name}"


class MongoDBRepository:

    def __init__(self, database: str, config: MongoDBConfig) -> None:
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

    def get_collection(self, collection_name: str) -> Collection:
        """Get a specific collection from the database."""
        return self.db[collection_name]

    def get_document_from_collection(self, collection_name: str, query: Optional[Dict] = None) -> List[Dict]:
        """Retrieve data from a specific collection."""
        collection = self.get_collection(collection_name)
        if query is None:
            return list(collection.find())
        return list(collection.find(query))

    def filter_document_by_user_name(self, collection_name: str, user_name: str) -> dict:
        """Retrieve data for a specific user from a collection."""
        collection = self.get_collection(collection_name)
        query = {'_id': user_name}
        return collection.find_one(query)

    def filter_document_by_meeting_id(self, meeting_id: str) -> dict:
        collection = self.get_collection(collection_name='meetings')
        print(collection)
        _id = collection.find_one({'_id': ObjectId(meeting_id)})
        return _id

    def write_document_to_collection(self, *, collection_name: str, document: Dict) -> None:
        """Write a document to a specific collection."""
        collection = self.get_collection(collection_name)
        collection.insert_one(document)


class MongoDBRetentionUtils(MongoDBRepository):

    def get_retention_period_from(self, user_name: str, collection_name: Literal['USER_SETTINGS', 'SYSTEM', 'MEETINGS']) -> int:
        """
        example output:
            {
                period: 0, < ------------ gets from here
                canExtend: False,
                type: 'User'
            }
        """
        match collection_name:

            case 'SYSTEM':
                collection = self.get_document_from_collection(collection_name="system")
                return collection[0]['retention']

            case 'MEETINGS':
                collection = self.filter_document_by_user_name(user_name=user_name, collection_name="meetings")
                return collection['retention']['extension']['period']

            case 'USER_SETTINGS':
                collection = self.filter_document_by_user_name(user_name=user_name, collection_name="userSettings")
                return collection['userProfile']['retention']['period']

            case _:
                raise ValueError(f"Invalid collection name: {collection_name}. Expected 'SYSTEM' or 'MEETINGS'.")

    def set_retention_period_in(self,
                                user_name: str,
                                collection_name: Literal['USER_SETTINGS', 'SYSTEM', 'MEETINGS'],
                                new_period: int
                                ) -> int:
        """
        example output:
            {
                period: 0, < ------------ gets from here
                canExtend: False,
                type: 'User'
            }
        """
        match collection_name:

            case 'USER_SETTINGS':

                try:
                    collection = self.get_collection("userSettings")

                    existing_doc = collection.find_one({'_id': user_name}, {'_id': 1})
                    if not existing_doc:
                        log.error(f"User '{user_name}' not found in userSettings collection")
                        return False

                    result = collection.update_one(upsert=False,  # **important to avoid creating a new document**
                                                   filter={'_id': user_name},
                                                   update={'$set': {'retention.period': new_period}})

                    if result.modified_count > 0:
                        log.warning(f"Updated retention period to {new_period} for user {user_name}")
                        return True
                    else:
                        log.warning(f"No document found for user {user_name}")
                        return False

                except Exception as e:
                    log.error(f"Error updating retention period: {e}")
                    return False

            case _:
                raise ValueError(f"Invalid collection name: {collection_name}. Expected 'SYSTEM' or 'MEETINGS'.")

    def get_retention_extend_status(self, user_name: str, collection_name: Literal['USER_SETTINGS', 'SYSTEM', 'MEETINGS']) -> int:
        """
        example output:
            {
                period: 0,
                canExtend: False, < ------------ gets from here
                type: 'User'
            }
        """
        match collection_name:

            case 'USER_SETTINGS':
                collection = self.filter_document_by_user_name(user_name=user_name, collection_name="userSettings")
                return collection['userProfile']['retention']['canExtend']

            case _:
                raise ValueError(f"Invalid collection name: {collection_name}. Expected 'SYSTEM' or 'MEETINGS'.")

    def get_retention_last_sync_time(self, user_name: str, collection_name: Literal['USER_SETTINGS', 'SYSTEM', 'MEETINGS']) -> int:
        """
        example output:
            {
                isSync: False,
                lasySync: 'time' < ------------ gets from here
            }
        """
        match collection_name:

            case 'USER_SETTINGS':
                collection = self.filter_document_by_user_name(user_name=user_name, collection_name="userSettings")
                return collection['userProfile']['retention']['status']['lastSync']

            case _:
                raise ValueError(f"Invalid collection name: {collection_name}. Expected 'SYSTEM' or 'MEETINGS'.")
