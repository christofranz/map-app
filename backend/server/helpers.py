import requests

def query_overpass_api(query):
    """TODO"""
    overpass_url = "http://overpass-api.de/api/interpreter"
    response = requests.get(overpass_url, 
                        params={'data': query})
    data = response.json()
    return data


def convert_to_geo_dict(data):
    """TODO"""
    return { "type": "FeatureCollection",
                        "features": [ 
                                        {"type": "Feature",
                                         "geometry": { "type": "LineString",
                                                       "coordinates": [ [point['lon'],
                                                                        point['lat']] for point in feature["geometry"]]},
                                         "properties": { key: value 
                                                         for key, value in feature.items()
                                                         if key != "geometry" }
                                         } 
                                     for feature in data["elements"]
                                    ]
                       }