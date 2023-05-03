#!/usr/bin/python3
"""States API routes"""

from flask import Flask, jsonify, request, current_app
from api.v1.views import app_views
from models import storage, State

states = current_app.blueprints['states']


@states.route('/', methods=['GET'])
def get_states():
    """Retrieves the list of all State objects"""
    return jsonify([state.to_dict() for state in storage.all('State').values()])


@states.route('/<state_id>', methods=['GET'])
def get_state(state_id):
    """Retrieves a State object"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@states.route('/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Deletes a State object"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@states.route('/', methods=['POST'])
def create_state():
    """Creates a State"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    state = State(**request.get_json())
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201


@states.route('/<state_id>', methods=['PUT'])
def update_state(state_id):
    """Updates a State object"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
