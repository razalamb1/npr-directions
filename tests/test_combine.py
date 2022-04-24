"""Test combining Google Maps and NPR data."""

from src.combine import get_lines
from dotenv import load_dotenv
import googlemaps
import os

load_dotenv()


def test_get_line():
    """Test function getting line objects."""
    GMAPS_KEY = os.environ.get("GMAPS_KEY")
    NPR_KEY = os.environ.get("NPR_KEY")
    client = googlemaps.Client(key=GMAPS_KEY)
    gdf = get_lines(client, NPR_KEY, "Durham, NC", "Chapel Hill, NC")
    assert gdf.iloc[0, 0] == "WUNC FM 91.5"
    pass
