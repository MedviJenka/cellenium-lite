import os
from time import sleep
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

    def filter_document_by_user_name(self, collection_name: str, user_email: str) -> dict:
        """Retrieve data for a specific user from a collection."""
        collection = self.get_collection(collection_name)
        query = {'_id': user_email}
        return collection.find_one(query)

    def filter_document_by_meeting_id(self, meeting_id: str) -> dict:
        collection = self.get_collection(collection_name='meetings')
        print(collection)
        _id = collection.find_one({'_id': ObjectId(meeting_id)})
        return _id

    def write_value_in_collection(self,
                                  *,
                                  collection_name: str,
                                  filter_by: dict,
                                  path: str,
                                  new_value: any) -> any:

        """
        Updates a specific field value in a MongoDB collection document.

        Finds a document matching the filter criteria and updates the specified
        field path with a new value. Does not create new documents if no match
        is found (upsert=False).

        Returns:
        bool: True if a document was successfully modified, False if no
             matching document was found or no changes were made.

        Example 1:
        # Update user's retention period
        success = db.write_value_in_collection(
           collection_name="userSettings",
           filter_by={"_id": "user@example.com"},
           path="userProfile.retention.period",
           new_value=30
        )

        Example 2:
        # Update user's retention period
        success = db.write_value_in_collection(
           collection_name="userSettings",
           filter_by={"_id": ObjectId("123456789")},
           path="userProfile.retention.period",
           new_value=30
        )
        """
        try:
            result = self.get_collection(collection_name=collection_name).update_one(
                filter=filter_by,
                update={'$set': {path: new_value}},
                upsert=False)  # **:IMPORTANT:** Don't create a new document if user doesn't exist
            return result

        except Exception as e:
            log.error(f"Error updating retention period: {e}")
            raise

        finally:
            sleep(1.5)


class MongoDBRetentionUtils(MongoDBRepository):

    def get_retention_period_from(self, user_email: str, collection_name: Literal['USER_SETTINGS', 'SYSTEM', 'MEETINGS']) -> int:
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
                collection = self.filter_document_by_user_name(user_email=user_email, collection_name="meetings")
                return collection['retention']['extension']['period']

            case 'USER_SETTINGS':
                collection = self.filter_document_by_user_name(user_email=user_email, collection_name="userSettings")
                return collection['userProfile']['retention']['period']

            case _:
                raise ValueError(f"Invalid collection name: {collection_name}. Expected 'SYSTEM' or 'MEETINGS'.")

    def set_retention_period_in(self,
                                user_email: str,
                                collection_name: Literal['USER_SETTINGS', 'SYSTEM', 'MEETINGS'],
                                new_period: int
                                ) -> None:  # Changed return type to bool since you're returning True/False
        """Sets the retention period for a user in the specified collection."""
        match collection_name:

            case 'USER_SETTINGS':
                result = self.write_value_in_collection(
                    collection_name="userSettings",
                    filter_by={"_id": user_email},
                    path="userProfile.retention.period",
                    new_value=new_period
                )
                if result.modified_count > 0:
                    log.warning(f"Updated retention period to {new_period}")
                    raise

                if not result:
                    raise ValueError(f"Failed to set retention period for {user_email} in {collection_name}")
            case _:
                raise ValueError(
                    f"Invalid collection name: {collection_name}. Expected 'USER_SETTINGS', 'SYSTEM', or 'MEETINGS'.")

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
                collection = self.filter_document_by_user_name(user_email=user_name, collection_name="userSettings")
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
                collection = self.filter_document_by_user_name(user_email=user_name, collection_name="userSettings")
                return collection['userProfile']['retention']['status']['lastSync']

            case _:
                raise ValueError(f"Invalid collection name: {collection_name}. Expected 'SYSTEM' or 'MEETINGS'.")
