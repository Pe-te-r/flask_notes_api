from flask import jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.database.Model import Notes,User


notes_bp = Blueprint('notes_bp',__name__)

@notes_bp.route('/notes', methods=['GET'])
def get_notes():
    notes = Notes.get_all_notes()
    if notes:
        return jsonify({'notes': [note.to_json() for note in notes]})
    return jsonify({'error': 'no notes found'})

@notes_bp.route('/notes/<note_id>',methods=['GET'])
@jwt_required()
def get_one_note(note_id):
    email = get_jwt_identity()
    user = User.get_by_email(email)
    print(user)

    note= Notes.get_by_id(note_id)
    print(note)
    if note:
        return jsonify(note.to_json())
    return jsonify({'error': 'no note found'})

@notes_bp.route('/notes',methods=['POST'])
@jwt_required()
def create_notes():
    try:
        email = get_jwt_identity()
        user = User.get_by_email(email)
        if not user:
            return jsonify({'error':'user not found'})
        note = Notes.create_note(user.id,'this is my first note here')
        print(note)
        if note:
            return jsonify({'notes': note.to_json()})
        return jsonify({'error': 'error creating notes'})

    except Exception:
        return jsonify({'notes': 'error creating notes'})

@notes_bp.route('/notes/<note_id>',methods=['DELETE'])
def delete_notes(note_id):
    note = Notes.delete_note(note_id)
    if note:
        return jsonify({'message': 'note deleted'})
    return jsonify({'error': 'note not found'})
