import requests
import random
from osm2geojson import json2geojson


def query_overpass_api(query):
    """Query overpass api.

    Args:
        query (str): Query to be send to overpass api.

    Returns:
        dict: Response of the query.
    """
    overpass_url = "http://overpass-api.de/api/interpreter"
    response = requests.get(overpass_url, 
                        params={'data': query})
    data = response.json()
    return data


GRAYS = [
"#000000",
"#080808",
"#101010",
"#181818",
"#202020",	
"#282828",
"#303030",
"#383838",
"#404040",
"#484848",
"#505050",
"#585858",
"#606060",
"#686868",
"#696969",
"#707070",
"#787878",
"#808080",
"#888888",
"#909090",
"#989898",
"#A0A0A0",
"#A8A8A8",
"#A9A9A9",
"#B0B0B0",
"#B8B8B8",	
"#BEBEBE",
"#C0C0C0",
"#C8C8C8",
"#D0D0D0",
"#D3D3D3",
"#D8D8D8",
"#DCDCDC",
"#E0E0E0",
"#E8E8E8",
"#F0F0F0",
"#F5F5F5",
"#F8F8F8"]


def get_radom_gray():
    """Generate a semi-random gray color.

    Args:

    Returns:
        str: Gray color as hex string.
    """
    return GRAYS[random.randint(0, len(GRAYS)-1)]


def convert_relations_to_geodict(data):
    """Convert OSM relations to geojson dict.

    Args:
        data (json): Overpass api response containig relations.

    Returns:
        dict: Relations as geojson objects within a dict.
        array: Lateral and longitudinal bounds of all relations.
    """
    geodict = json2geojson(data)
    # determine the geometrical bounds of the relations used in the frontend
    lat_min, lat_max, lon_min, lon_max = 10000, -10000, 10000, -10000
    for feature in geodict["features"]:
        relation_color = get_radom_gray()
        feature["properties"].update({"color": relation_color})
        if feature["geometry"]["type"] == "LineString":
            coordinates = feature["geometry"]["coordinates"]
        elif feature["geometry"]["type"] == "MultiLineString":
            coordinates = []
            for c in feature["geometry"]["coordinates"]:
                coordinates += c
        else:
            raise ValueError(feature["geometry"]["type"])
        
        f_lat_min = min([x[1] for x in coordinates])
        f_lat_max = max([x[1] for x in coordinates])
        f_lon_min = min([x[0] for x in coordinates])
        f_lon_max = max([x[0] for x in coordinates])

        if lat_min > f_lat_min:
            lat_min = f_lat_min
        if lat_max < f_lat_max:
            lat_max = f_lat_max
        if lon_min > f_lon_min:
            lon_min = f_lon_min
        if lon_max < f_lon_max:
            lon_max = f_lon_max

    bounds = [[lat_min, lon_min], [lat_max, lon_max]]
    return geodict, bounds