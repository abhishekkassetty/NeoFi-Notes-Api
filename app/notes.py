from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import Note, User, NoteVersion
from . import db

notes_bp = Blueprint('notes', __name__)

@notes_bp.route('/notes/create', methods=['POST'])
@jwt_required()
def create_note():
    current_user_id = get_jwt_identity()
    data = request.get_json()

    title = data.get('title')
    text = data.get('text')

    if not title or not text:
        return jsonify({'error': 'Missing required fields'}), 400

    new_note = Note(title=title, text=text, user_id=current_user_id)
    db.session.add(new_note)
    db.session.commit()

    return jsonify({'message': 'Note created successfully'}), 201

@notes_bp.route('/notes/<int:id>', methods=['GET'])
@jwt_required()
def get_note(id):
    current_user_id = get_jwt_identity()

    note = Note.query.filter_by(id=id, user_id=current_user_id).first()

    if not note:
        return jsonify({'error': 'Note not found'}), 404

    return jsonify({'id': note.id, 'title': note.title, 'text': note.text, 'user_id': note.user_id})

@notes_bp.route('/notes/share', methods=['POST'])
@jwt_required()
def share_note():
    current_user_id = get_jwt_identity()
    data = request.get_json()

    note_id = data.get('note_id')
    users = data.get('users')

    note = Note.query.filter_by(id=note_id, user_id=current_user_id).first()

    if not note:
        return jsonify({'error': 'Note not found'}), 404

    for user_id in users:
        user = User.query.get(user_id)
        if user:
            note.shared_with.append(user)

    db.session.commit()

    return jsonify({'message': 'Note shared successfully'}), 200

@notes_bp.route('/notes/<int:id>', methods=['PUT'])
@jwt_required()
def update_note(id):
    current_user_id = get_jwt_identity()
    data = request.get_json()

    new_text = data.get('new_text')

    if not new_text:
        return jsonify({'error': 'Missing required field'}), 400

    note = Note.query.filter_by(id=id, user_id=current_user_id).first()

    if not note:
        return jsonify({'error': 'Note not found'}), 404

    # Assuming no existing sentences can be edited, and new sentences can be added
    note.text += "\n" + new_text

    db.session.commit()

    return jsonify({'message': 'Note updated successfully'}), 200

@notes_bp.route('/notes/version-history/<int:id>', methods=['GET'])
@jwt_required()
def get_version_history(id):
    current_user_id = get_jwt_identity()
    note = Note.query.filter_by(id=id, user_id=current_user_id).first()

    # Check if the note exists and is owned by the current user
    if not note:
        return jsonify({'error': 'Note not found'}), 404

    # Fetch the version history for the note
    version_history = NoteVersion.query.filter_by(note_id=note.id).all()
    print(version_history)
    # Prepare the response
    response = {
        'note_id': note.id,
        'title': note.title,
        'text': note.text,
        'version_history': [{
            'timestamp': version.timestamp,
            'user_id': version.user_id,
            'changes': version.changes
        } for version in version_history]
    }


    return jsonify(response), 200
