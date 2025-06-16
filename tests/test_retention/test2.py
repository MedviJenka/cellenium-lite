import os
import pytest
from typing import Literal, Optional, Dict, Any, List

from bson import ObjectId
from pydantic import Field
from dotenv import load_dotenv
from pymongo import MongoClient
from pydantic import computed_field
from functools import cached_property
from pydantic_settings import BaseSettings
from pymongo.synchronous.database import Database
from pymongo.collection import Collection


load_dotenv("mongo.env")

# devming
# DATABASE_ID = "05f68ce2-ee68-4bfc-8b6e-60e5b34d95e0"

# aisquad01
DATABASE_ID = '5bc8f4b0-9734-4b95-a197-ae14a4e3d872'
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_CLUSTER = os.getenv("MONGO_CLUSTER")
MONGO_APP_NAME = os.getenv("MONGO_APP_NAME")


class Logger:

    def error(self, message: str) -> None:...

    def bug(self, message: str) -> None:
        print(f"BUG: {message}")

    def warning(self, message: str) -> None:
        print(f"WARNING: {message}")


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

    def get_data_from_collection(self, collection_name: str, query: Optional[Dict] = None) -> List[Dict]:
        """Retrieve data from a specific collection."""
        collection = self.get_collection(collection_name)
        if query is None:
            return list(collection.find())
        return list(collection.find(query))

    def get_data_from_specific_user(self, collection_name: str, user_name: str) -> dict:
        """Retrieve data for a specific user from a collection."""
        collection = self.get_collection(collection_name)
        query = {'_id': user_name}
        return collection.find_one(query)

    def get_collection_by_meeting_id(self, meeting_id: str) -> dict:
        collection = self.get_collection(collection_name='meetings')
        print(collection)
        _id = collection.find_one({'_id': ObjectId(meeting_id)})
        return _id


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
                collection = self.get_data_from_collection(collection_name="system")
                return collection[0]['retention']

            case 'MEETINGS':
                collection = self.get_data_from_specific_user(user_name=user_name, collection_name="meetings")
                return collection['retention']

            case 'USER_SETTINGS':
                collection = self.get_data_from_specific_user(user_name=user_name, collection_name="userSettings")
                return collection['userProfile']['retention']['period']

            case _:
                raise ValueError(f"Invalid collection name: {collection_name}. Expected 'SYSTEM' or 'MEETINGS'.")

    def get_retention_extend_status(self, user_name: str, collection_name: Literal['USER_SETTINGS', 'SYSTEM', 'MEETINGS']) -> bool:
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
                collection = self.get_data_from_specific_user(user_name=user_name, collection_name="userSettings")
                return collection['userProfile']['retention']['canExtend']

            case _:
                raise ValueError(f"Invalid collection name: {collection_name}. Expected 'SYSTEM' or 'MEETINGS'.")

    def get_retention_last_sync_time(self, user_name: str, collection_name: Literal['USER_SETTINGS', 'SYSTEM', 'MEETINGS']) -> bool:
        """
        example output:
            {
                isSync: true
                lastSync: 1234T213 <------------ gets from here

            }
        """
        match collection_name:

            case 'USER_SETTINGS':
                collection = self.get_data_from_specific_user(user_name=user_name, collection_name="userSettings")
                return collection['userProfile']['retention']['status']['lastSync']

            case _:
                raise ValueError(f"Invalid collection name: {collection_name}. Expected 'SYSTEM' or 'MEETINGS'.")


@pytest.fixture(scope='session')
def db_utils() -> MongoDBRetentionUtils:
    """Fixture to provide a MongoDBRetentionUtils instance for testing."""
    config = MongoDBConfig()
    return MongoDBRetentionUtils(database=DATABASE_ID, config=config)


class TestRetention:

    """
    TODO:
        ** retention period **
        scenario 1. navigate to user profile and set retention from default to 2 years
        validate in DB: user settings -> user profile -> user -> retention -> period changed to 730 .................................................. DONE
        scenario 2. ui -> check extend flag -> (as above) -> period changed extend flag set to true & validate datetime in last sync ................. DONE
        scenario 3. ui -> check media / ai / transcription -> (as above) -> period changed extend flag set to false .................................. DONE
        scenario 4. ui -> list view -> choose meeting -> click on ...  -> (not implement yet) -> DB -> validate meeting retention
        scenario 5. teams call -> side panel -> extend  -> (not implement yet) -> DB -> validate meeting retention
        ---
        ** zero retention period **
        scenario 1. zero retention media period -> validate with bini that media is deleted and only audio left

    Test suite for retention functionality.

    Test Scenarios:

    ** Retention Period Tests **
    1. User profile retention change: default → 2 years
       - Validate: userSettings.userProfile.user.retention.period = 730 days ............... DONE

    2. UI extend flag enabled:
       - Validate: period changed, extend_flag = True, last_sync datetime updated

    3. UI media/AI/transcription settings:
       - Validate: period changed, extend_flag = False

    4. Meeting-specific retention (list view):
       - Validate: individual meeting retention settings

    5. Teams call side panel extend:
       - Validate: meeting-specific retention via side panel

    ** Zero Retention Tests **
    1. Zero retention media period:
       - Validate: media deleted, only audio remains (coordinate with Bini)

    Database: {DATABASE_ID}
    Host: aisquad01-pri.hpbna7.mongodb.net
    Collection: userSettings
    """

    @pytest.mark.dependency(name="test_database_connection")
    def test_database_connection(self, db_utils: MongoDBRetentionUtils) -> None:
        """
        Test that database connection is established and collections are accessible.

        **IMPORTANT NOTICE**
        If this fails, other tests will not run, so please check your mongo.env file
        """
        collections = db_utils.db.list_collection_names()

        assert isinstance(collections, list), "Collections should be returned as a list"
        assert len(collections) > 0, "Database should contain at least one collection"
        assert "userSettings" in collections, "userSettings collection should exist"

    @pytest.mark.dependency(depends=["test_database_connection"])
    def test_user_settings_collection_exists(self, db_utils: MongoDBRetentionUtils) -> None:
        """Test that the userSettings collection exists and is accessible."""
        collection = db_utils.db["userSettings"]
        count = collection.count_documents({})
        assert count > 0, "Should be able to count documents in userSettings"
        log.bug("userSettings collection validated successfully")

    @pytest.mark.dependency(depends=["test_database_connection"])
    def test_retention_period_change_default_to_two_years(self, db_utils: MongoDBRetentionUtils) -> None:
        """TODO: Implement UI automation"""
        user_email = "QA_Auto_user_Teams_4@ai-logix.net"
        document = db_utils.get_retention_period_from(user_name=user_email, collection_name="USER_SETTINGS")
        assert document is not None, log.warning(f"User document should not be None for {user_email}")
        assert document is 730, log.bug(f"Retention period should be 730 days for {user_email}")

    @pytest.mark.dependency(depends=["test_database_connection"])
    def test_retention_extend_flag_enabled(self, db_utils: MongoDBRetentionUtils) -> None:
        """
        TODO:
            scenario 2. ui -> check extend flag -> (as above) -> period changed extend flag set to true & validate datetime in last sync
        Test enabling extend flag and validating database changes.

        Steps:
        1. UI: Check extend flag
        2. Validate: period changed, extend_flag = True, last_sync datetime updated
        """
        # TODO: Implement UI automation
        # TODO: Validate extend_flag = True
        # TODO: Validate last_sync datetime
        """TODO: Implement UI automation"""
        user_email = "QA_Auto_user_Teams_4@ai-logix.net"
        expected = False
        status = db_utils.get_retention_extend_status(user_name=user_email, collection_name="USER_SETTINGS")
        lasy_sync = db_utils.get_retention_last_sync_time(user_name=user_email, collection_name="USER_SETTINGS")

        assert status is expected, log.bug(f"Extend flag should not be {expected} for {user_email}")
        assert lasy_sync is 'IMPLEMENT DATE TIME', log.bug(f"Extend flag should not be {expected} for {user_email}")

    @pytest.mark.dependency(depends=["test_database_connection"])
    def test_retention_media_ai_transcription_settings(self, db_utils: MongoDBRetentionUtils) -> None:
        """
        Test media/AI/transcription retention settings.

        Steps:
        1. UI: Configure media/AI/transcription settings
        2. Validate: period changed, extend_flag = False
        """
        user_email = "QA_Auto_user_Teams_4@ai-logix.net"
        expected = False
        status = db_utils.get_retention_extend_status(user_name=user_email, collection_name="USER_SETTINGS")
        lasy_sync = db_utils.get_retention_last_sync_time(user_name=user_email, collection_name="USER_SETTINGS")

        assert status is expected, log.bug(f"Extend flag should not be {expected} for {user_email}")
        assert lasy_sync is 'IMPLEMENT DATE TIME', log.bug(f"Extend flag should not be {expected} for {user_email}")


    def test_meeting_specific_retention_list_view(self, db_utils: MongoDBRetentionUtils) -> None:
        """
        Test meeting-specific retention via list view.

        Steps:
        1. UI: Navigate to meeting list view
        2. Select meeting → click "..." → set retention
        3. Validate: meeting-specific retention in the database
        """
        # TODO: Wait for feature implementation
        # TODO: Implement UI automation
        # TODO: Validate meeting retention settings

        collection = db_utils.get_collection_by_meeting_id(meeting_id='682f103ba2642f6826a722ea')
        print(collection)

    @pytest.mark.skip(reason="Feature not implemented - Teams call side panel")
    def test_teams_call_side_panel_extend(self, db_utils: MongoDBRetentionUtils) -> None:
        """
        Test retention extension via Teams call side panel.

        Steps:
        1. Teams call: Access side panel
        2. Enable extend option
        3. Validate: meeting retention settings in database
        """
        # TODO: Wait for feature implementation
        # TODO: Implement Teams integration
        # TODO: Validate meeting retention settings
        pass

    @pytest.mark.skip(reason="Coordination required with Bini team")
    def test_zero_retention_media_deletion(self, db_utils: MongoDBRetentionUtils) -> None:
        """
        Test zero retention period media deletion.

        Steps:
        1. Set zero retention media period
        2. Validate: media files deleted, only audio remains

        Note: Requires coordination with Bini team for media validation
        """
        # TODO: Coordinate with Bini team
        # TODO: Implement media deletion validation
        # TODO: Validate audio files remain
        pass

    # Helper methods for future implementation
    def _get_user_retention_settings(self, db_utils: MongoDBRetentionUtils, user_id: str) -> Optional[Dict]:
        """Helper method to retrieve user retention settings from database."""
        return db_utils.get_data_from_specific_user(collection_name="userSettings", user_name=user_id)

    def _validate_retention_period(self, settings: Dict, expected_days: int) -> bool:
        """Helper method to validate retention period in settings."""
        try:
            period = settings["userProfile"]["retention"]["period"]
            return period == expected_days
        except (KeyError, TypeError):
            return False

    def _validate_extend_flag(self, settings: Dict, expected_value: bool) -> bool:
        """Helper method to validate extend flag in settings."""
        try:
            extend_flag = settings["userProfile"]["retention"]["extend_flag"]
            return extend_flag == expected_value
        except (KeyError, TypeError):
            return False
