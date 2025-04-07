from flask import Blueprint, jsonify, request, abort
from .models import db, Episode, Guest, Appearance
import traceback

# create a blueprint for the API
api = Blueprint('api', __name__)

# GET all episodes
@api.route('/episodes', methods=['GET'])
def get_episodes():
    try:
        # get all episodes from DB
        all_episodes = Episode.query.all()
        # convert to list of dicts
        episodes_data = [ep.to_dict() for ep in all_episodes]
        return jsonify(episodes_data)
    except Exception as e:
        # log the error
        print(f"Error in get_episodes: {str(e)}")
        return jsonify({"error": "Failed to fetch episodes"}), 500

# GET specific episode by ID
@api.route('/episodes/<int:episode_id>', methods=['GET'])
def get_episode(episode_id):
    # find the episode
    episode = Episode.query.get(episode_id)
    
    # check if exists
    if not episode:
        return jsonify({"error": "Episode not found"}), 404
    
    # return detailed representation
    return jsonify(episode.to_dict(detailed=True))

# GET all guests
@api.route('/guests', methods=['GET'])
def get_guests():
    # simple - just get and return all guests
    guests = Guest.query.all()
    return jsonify([g.to_dict() for g in guests])

# POST a new appearance
@api.route('/appearances', methods=['POST'])
def create_appearance():
    # get json data
    data = request.get_json()
    
    # check if we have all required fields
    if not all(field in data for field in ['rating', 'episode_id', 'guest_id']):
        return jsonify({"errors": ["Missing required fields"]}), 400
    
    # check if episode exists
    episode = Episode.query.get(data['episode_id'])
    if not episode:
        return jsonify({"errors": [f"Episode with id {data['episode_id']} not found"]}), 404
    
    # check if guest exists
    guest = Guest.query.get(data['guest_id'])
    if not guest:
        return jsonify({"errors": [f"Guest with id {data['guest_id']} not found"]}), 404
    
    try:
        # create new appearance
        appearance = Appearance(
            rating=data['rating'],
            episode_id=data['episode_id'],
            guest_id=data['guest_id']
        )
        
        # add to db
        db.session.add(appearance)
        db.session.commit()
        
        # return the created object
        return jsonify(appearance.to_dict())
    
    except ValueError as e:
        # handle validation errors
        db.session.rollback()
        return jsonify({"errors": [str(e)]}), 400
    except Exception as e:
        # handle other errors
        db.session.rollback()
        print(f"Error creating appearance: {str(e)}")
        print(traceback.format_exc())
        return jsonify({"errors": ["Server error creating appearance"]}), 500