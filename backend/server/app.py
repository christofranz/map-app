from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from helpers import query_overpass_api, convert_to_geo_dict
import os

load_dotenv()

# Set up the app and point it to Vue
app = Flask(__name__, static_folder='../../frontend/dist/',    static_url_path='/')

# Set up the index route
@app.route('/')
def index():
    return app.send_static_file('index.html')

# configuration
# DEBUG = True

# instantiate the app
# app = Flask(__name__)
# app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# make overpass api query
# overpass_query = """
# [out:json];
# area[name="Stuttgart"];
# way["highway"="motorway"](area);
# out geom;
# """
# motorways = convert_to_geo_dict(query_overpass_api(overpass_query))

# @app.route('/motorways', methods=['GET'])
# def get_motorways_stuttgart():
#     return jsonify({
#         'status': 'success',
#         'motorways': motorways
#     })

@app.route('/motorways/<string:region>/', methods=['GET'])
def get_motorways(region):
    overpass_query = """
        [out:json];
        area[name="{}"];
        way["highway"="motorway"](area);
        out geom;
    """.format(region)
    print(overpass_query)
    motorways = convert_to_geo_dict(query_overpass_api(overpass_query))
    return jsonify({
        'status': 'success',
        'motorways': motorways
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)