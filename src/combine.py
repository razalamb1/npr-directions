"""Combine Google Maps and NPR."""

try:
    from src.gmaps import get_directions
    from src.npr import get_stations, StationError
except ModuleNotFoundError:
    from gmaps import get_directions
    from npr import get_stations, StationError
import googlemaps
import geopandas as gpd
from math import cos, asin, sqrt, pi
import shapely
import contextily as cx
import matplotlib


def distance(lat1, lon1, lat2, lon2):
    """Calculate distance given lat and lon."""
    p = pi / 180
    a = (
        0.5
        - cos((lat2 - lat1) * p) / 2
        + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    )
    return 12742 * asin(sqrt(a))


def ax_limits(geometry: list) -> tuple:
    """Determine whether to pad frame."""
    x = shapely.ops.linemerge(geometry)
    xmin, ymin, xmax, ymax = x.bounds
    ver = ymax - ymin
    hor = xmax - xmin
    ratio = hor / ver
    if ratio > 2:
        new = ver * ratio / 2
        buff = (new - ver) / 2
        return "ylim", (ymin - buff, ymax + buff)
    elif ratio < 0.5:
        new = 1 / (ratio * 2)
        buff = (new - hor) / 2
        return "xlim", (xmin - buff, xmax + buff)
    return None, None


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
    stations = []
    geometry = []
    check_dist = 60
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
            if dist > check_dist:
                stations.append(curr_st)
                points = gmaps.loc[curr_idx : i + 1, "geometry"].to_list()
                line = shapely.geometry.LineString(points)
                geometry.append(line)
                try:
                    temp_st, _ = get_stations(npr_key, lng, lat)
                    if temp_st == curr_st:
                        check_dist = 20
                        curr_st = temp_st
                    else:
                        check_dist = 60
                        curr_st = temp_st
                except StationError:
                    check_dist = 50
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
    return lines_df.dissolve(by="stations").reset_index()


def graph_lines(gdf: gpd.GeoDataFrame):
    """Graph NPR stations with Gmaps polyline."""
    matplotlib.rcParams.update({"font.size": 15})
    matplotlib.rcParams["font.family"] = "arial"
    ax = gdf.plot(
        figsize=(15, 15),
        column="stations",
        legend=True,
        linewidth=5,
        legend_kwds={
            "loc": "upper right",
            "framealpha": 1.0,
            "bbox_to_anchor": (1.22, 1),
            "handletextpad": 0.3,
        },
    )
    keyword, ax_range = ax_limits(list(gdf.explode(index_parts=True).geometry))
    if keyword == "xlim":
        ax.set_xlim(ax_range)
    elif keyword == "ylim":
        ax.set_ylim(ax_range)
    else:
        ax.margins(0.3, 0.3)
    cx.add_basemap(ax, crs=3857, source=cx.providers.CartoDB.Voyager)
    ax.axis("off")
    gdf.apply(
        lambda x: ax.annotate(
            text=x["stations"],
            xy=x.geometry.centroid.coords[0],
            ha="center",
            va="baseline",
            fontsize=12,
            bbox={
                "facecolor": "white",
                "alpha": 0.8,
                "pad": 2,
                "edgecolor": "none",
            },
        ),
        axis=1,
    )
    return ax.figure
