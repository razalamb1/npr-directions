"""Make calls to NPR API."""

import requests
from typing import Tuple


def get_stations(npr_key: str, lon: str, lat: str) -> Tuple[str, str]:
    """Make call to NPR Stations API."""
    headers = {"Authorization": f"Bearer {npr_key}"}
    params = {"lat": lat, "lon": lon}
    url = "https://station.api.npr.org/v3/stations"
    r = requests.get(url, headers=headers, params=params, timeout=15).json()["items"]
    if len(r) == 0:
        raise StationError("No station returned by API.")
    st_one = r[0]["attributes"]["brand"]
    st_id = f"{st_one['call']} {st_one['band']} {st_one['frequency']}"
    city = f"{st_one['marketCity']}, {st_one['marketState']}"
    return (st_id, city)


class StationError(Exception):
    """No station returned by API."""
