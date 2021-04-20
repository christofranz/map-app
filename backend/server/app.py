from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
# in order to run the backend server also individually
try:
    from backend.server.helpers import query_overpass_api, convert_relations_to_geodict
except ImportError:
    from helpers import query_overpass_api, convert_relations_to_geodict
import os
from geopy.geocoders import Nominatim

load_dotenv()

# Set up the app and point it to Vue
app = Flask(__name__, static_folder='../../frontend/dist/',    static_url_path='/')

# Set up the index route
@app.route('/')
def index():
    """Connect index from vue app."""
    return app.send_static_file('index.html')

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/hiking/<string:region>/', methods=['GET'])
def get_hiking_routes(region):
    """Get hiking routes for the requested region.

    Args:
        region (str): Region for which to find the hiking routes.

    Returns:
        json: Response containing the status, routes and bounds.
    """
    # Geocoding request via Nominatim
    geolocator = Nominatim(user_agent="city_compare")
    geo_results = geolocator.geocode(region, exactly_one=False, limit=3)

    # Searching for relation in result set
    for r in geo_results:
        if r.raw.get("osm_type") == "relation":
            city = r
            break

    # Calculating area id
    area_id = int(city.raw.get("osm_id")) + 3600000000
    overpass_query = """
    [out:json];
    area({})->.searchArea;
    relation(area.searchArea)[route=hiking];
    out geom;
    """.format(area_id)
    query_result = query_overpass_api(overpass_query)
    routes, bounds = convert_relations_to_geodict(query_result)
    return jsonify({
        'status': 'success',
        'routes': routes,
        'bounds': bounds
    })


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)