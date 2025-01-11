from utils.option_loader import OptionLoader
from utils.loggers import DebugLogger, TestLogger
import pytest
import time
from pathlib import Path

test_logger_instance = TestLogger()

@pytest.fixture(scope="session")
def settings() -> OptionLoader:
    """Session-level fixture providing access to test settings.
    
    This fixture initializes the OptionLoader which manages test configuration
    settings from configs.json. The configuration is loaded once at the start 
    of the test session and shared across all tests.        
    Raises:
        FileNotFoundError: If configs.json doesn't exist
        json.JSONDecodeError: If configs.json is not valid JSON
    """
    return OptionLoader()


@pytest.fixture(scope="session")
def test_logger():
    """Session-level fixture providing the test logger instance"""
    return test_logger_instance
