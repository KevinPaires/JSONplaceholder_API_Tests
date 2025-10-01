import pytest
import os
from dotenv import load_dotenv


load_dotenv()


@pytest.fixture(scope="session")
def base_url():
    """Base URL for the API - can be overridden with environment variable"""
    return os.getenv("API_BASE_URL", "https://jsonplaceholder.typicode.com")


@pytest.fixture(scope="session")
def api_headers():
    """Common headers for API requests"""
    return {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }



@pytest.fixture
def valid_user_payload():
    """Valid user data for testing"""
    return {
        "name": "John Doe",
        "username": "johndoe",
        "email": "john.doe@example.com"
    }


@pytest.fixture
def valid_post_payload():
    """Valid post data for testing"""
    return {
        "title": "Test Post",
        "body": "This is a test post content",
        "userId": 1
    }

