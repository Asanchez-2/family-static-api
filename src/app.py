"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, json
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_all_members():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "family": members
    }
    return jsonify(response_body), 200

@app.route('/members/<id>', methods=['GET'])
def handle_single_member(id):
    member = jackson_family.get_member(id)
    response_body = {
        "family": member
    }
    if member:
        return jsonify(response_body), 200
    else: 
        return "Member not found", 400

@app.route('/member/<int:id>', methods=['DELETE'])
def delete_single_member(id):
    member_to_show = jackson_family.get_member(id)
    member_to_delete = jackson_family.delete_member(id)
    return jsonify(member_to_show), 200

@app.route('/member', methods=['POST'])
def add_single_member():
    requests_body = json.loads(request.data)
    member_to_add = jackson_family.add_member(requests_body)
    return jsonify(requests_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
