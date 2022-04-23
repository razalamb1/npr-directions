"""Make calls to Goole Maps API."""

import googlemaps
import pandas as pd
import geopandas as gpd
import shapely
import contextily as cx
from dotenv import dotenv_values


def get_directions(
    client: googlemaps.Client,
    origin: str,
    dest: str,
) -> gpd.GeoDataFrame:
    """Get directions JSON from GoogleMaps givin origin and destination."""
    results = client.directions(origin=origin, destination=dest)[0]
    legs = results["legs"][0]
    rq = "USA"
    if (legs["start_address"][-3:] != rq) | (legs["end_address"][-3:] != rq):
        raise OutsideUSA("Origin and dest must be inside the United States.")
    df = pd.DataFrame(
        googlemaps.convert.decode_polyline(
            results["overview_polyline"]["points"],
        )
    )
    gdf = (
        gpd.GeoDataFrame(
            df,
            geometry=gpd.points_from_xy(
                df.lng,
                df.lat,
            ),
        )
        .set_crs(epsg=4326)
        .to_crs(epsg=3857)
    )
    return gdf


class OutsideUSA(Exception):
    """Origin and destination must be inside the United States."""
