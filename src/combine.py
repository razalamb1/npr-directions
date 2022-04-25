"""Combine Google Maps and NPR."""

try:
    from src.gmaps import get_directions
    from src.npr import get_stations
except ModuleNotFoundError:
    from gmaps import get_directions
    from npr import get_stations
import googlemaps
import geopandas as gpd
from math import cos, asin, sqrt, pi
import shapely
import contextily as cx


def distance(lat1, lon1, lat2, lon2):
    """Calculate distance given lat and lon."""
    p = pi / 180
    a = (
        0.5
        - cos((lat2 - lat1) * p) / 2
        + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    )
    return 12742 * asin(sqrt(a))


def get_lines(
    client: googlemaps.Client,
    npr_key: str,
    origin: str,
    dest: str,
) -> gpd.GeoDataFrame:
    """Get station lines."""
    gmaps = get_directions(client, origin, dest)
    points = gmaps["geometry"]
    df_len = gmaps.shape[0]
    curr_st = None
    emer_stop = 1
    stations = []
    geometry = []
    for i in range(df_len):
        if curr_st is None:
            lng = gmaps.loc[i, "lng"]
            lat = gmaps.loc[i, "lat"]
            curr_st, _ = get_stations(npr_key, lng, lat)
            curr_idx = i
            st_origin = (gmaps.loc[i, "lng"], gmaps.loc[i, "lat"])
        else:
            lng = gmaps.loc[i, "lng"]
            lat = gmaps.loc[i, "lat"]
            dist = distance(st_origin[1], st_origin[0], lat, lng)
            if dist > 60:
                stations.append(curr_st)
                points = gmaps.loc[curr_idx : i + 1, "geometry"].to_list()
                line = shapely.geometry.LineString(points)
                geometry.append(line)
                if emer_stop > 3:
                    break
                curr_st, _ = get_stations(npr_key, lng, lat)
                emer_stop += 1
                curr_idx = i
                st_origin = (lng, lat)
        if i == df_len - 1:
            stations.append(curr_st)
            points = gmaps.loc[curr_idx:, "geometry"].to_list()
            line = shapely.geometry.LineString(points)
            geometry.append(line)
    lines_df = gpd.GeoDataFrame(
        {"stations": stations, "geometry": geometry},
        crs=3857,
    )
    return lines_df


def graph_lines(gdf: gpd.GeoDataFrame):
    """Graph NPR stations with Gmaps polyline."""
    ax = gdf.plot(
        figsize=(15, 15),
        column="stations",
        legend=True,
        linewidth=5,
        legend_kwds={"loc": "lower right"},
    )
    cx.add_basemap(ax, source=cx.providers.Stamen.TonerLite)
    ax.axis("off")
    return ax.figure
