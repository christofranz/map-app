from flask import Flask, jsonify
from flask_cors import CORS

from helpers import query_overpass_api, convert_to_geo_dict

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# make overpass api query
overpass_query = """
[out:json];
area[name="Stuttgart"];
way["highway"="motorway"](area);
out geom;
"""
motorways = convert_to_geo_dict(query_overpass_api(overpass_query))

@app.route('/motorways', methods=['GET'])
def all_books():
    return jsonify({
        'status': 'success',
        'motorways': motorways
    })


if __name__ == '__main__':
    app.run()