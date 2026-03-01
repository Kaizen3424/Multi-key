"""
Pytest configuration and fixtures
"""
import sys
import os
import pytest
import asyncio
import tempfile
from pathlib import Path

# Add the parent directory to Python path so we can import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

import requests

# Base URL for API testing
BASE_URL = "http://localhost:8000/api/v1"


@pytest.fixture(scope="session")
def event_loop():
    """Create an event loop for the test session."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def client():
    """Create requests session"""
    session = requests.Session()
    # Don't set default Content-Type to allow multipart/form-data for file uploads
    return session
