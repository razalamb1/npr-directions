"""Test Google Maps Interface."""

import pytest
from src.gmaps import get_directions, OutsideUSA
import googlemaps
from dotenv import dotenv_values


def test_get_directions():
    """Test get directions function."""
    config = dotenv_values(".env")
    GMAPS_KEY = config["GMAPS_KEY"]
    client = googlemaps.Client(key=GMAPS_KEY)
    with pytest.raises(OutsideUSA):
        get_directions(client, "Toronto, ON", "Chicago, IL")
    results = get_directions(client, "Chicago, IL", "Durham, NC")
    assert results.shape == (219,3)

if __name__ == "__main__":
    test_get_directions()
