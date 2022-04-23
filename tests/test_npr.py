"""Test NPR API Interface."""

from src.npr import get_stations, StationError
from dotenv import dotenv_values
import pytest


def test_get_stations():
    """Test get stations function."""
    config = dotenv_values(".env")
    NPR_KEY = config["NPR_KEY"]
    assert NPR_KEY is not None
    with pytest.raises(StationError):
        get_stations(NPR_KEY, "-99.67", "27.73")
    id, city = get_stations(NPR_KEY, "-78.99", "35.98")
    assert id == "WUNC FM 91.5"
    assert city == "Chapel Hill"
