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


COLORS = [
"#B0E0E6",
"#ADD8E6",
"#87CEFA",
"#87CEEB",
"#00BFFF",
"#B0C4DE",
"#1E90FF",
"#6495ED",
"#4682B4",
"#4169E1",
"#0000FF",
"#0000CD",
"#00008B",
"#000080",
"#191970",
"#7B68EE",
"#6A5ACD",
"#483D8B",
"#E6E6FA",
"#D8BFD8",
"#DDA0DD",
"#EE82EE",
"#DA70D6",
"#FF00FF",
"#FF00FF",
"#BA55D3",
"#9370DB",
"#8A2BE2",
"#9400D3",
"#9932CC",
"#8B008B",
"#800080",
"#4B0082"
]


def get_radom_gray():
    """Generate a semi-random gray color.

    Args:

    Returns:
        str: Gray color as hex string.
    """
    return COLORS[random.randint(0, len(COLORS)-1)]


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