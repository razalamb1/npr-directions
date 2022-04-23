"""Make calls to NPR API."""

from dotenv import dotenv_values
import requests


def get_stations(npr_key: str, lon: str, lat: str) -> tuple[str, str]:
    """Make call to NPR Stations API."""
    headers = {"Authorization": f"Bearer {npr_key}"}
    params = {"lat": lat, "lon": lon}
    url = "https://station.api.npr.org/v3/stations"
    r = requests.get(url, headers=headers, params=params).json()["items"]
    if len(r) == 0:
        raise StationError("No station returned by API.")
    print(r[0])
    st_one = r[0]["attributes"]["brand"]
    id = f"{st_one['call']} {st_one['band']} {st_one['frequency']}"
    city = f"{st_one['marketCity']}, {st_one['marketState']}"
    return (id, st_one["marketCity"])


class StationError(Exception):
    """No station returned by API."""
