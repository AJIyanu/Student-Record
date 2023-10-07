#!/usr/bin python3
"""
section loads local json object and returns json data
"""
import json

try:
    from flask_paths import app_views
except ModuleNotFoundError:
    from docs.flask_paths import app_views
from flask import jsonify


@app_views.route('/states', methods=['GET'])
def statesobj():
    """returns list of states object"""
    with open("docs/static/json/states.json", "r") as file:
        all_states = json.loads(file.read())
    states = [state['states']['name'] for state in all_states ]
    return jsonify(states)


@app_views.route('/lga/<state>', methods=['GET'])
def lgaobj(state):
    """returns list of lga onject according to state"""
    with open("docs/static/json/states.json", "r") as file:
        all_states = json.loads(file.read())
    if state is None:
        return jsonify(error="please provide state")
    lga = []
    for states in all_states:
        if state == states['states']['name']:
            lga = [lga['name'] for lga in states['states']['locals'] ]
    return jsonify(lga)
