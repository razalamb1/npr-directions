"""Test combining Google Maps and NPR data."""

from src.combine import get_line
from dotenv import dotenv_values
import googlemaps


def test_get_line():
    """Test function getting line objects."""
    config = dotenv_values(".env")
    GMAPS_KEY = config["GMAPS_KEY"]
    client = googlemaps.Client(key=GMAPS_KEY)

    pass
