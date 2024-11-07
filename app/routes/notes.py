from flask import jsonify, Blueprint
from app.database.Model import Notes


notes_bp = Blueprint('notes_bp',__name__)

@notes_bp.route('/notes', methods=['GET'])
def get_notes():
    notes = Notes.get_all_notes()
    if notes:
        return jsonify({'notes': [note.to_json() for note in notes]})
    return jsonify({'error': 'no notes found'})

@notes_bp.route('/notes/<note_id>',methods=['GET'])
def get_one_note(note_id):
    note= Notes.get_by_id(note_id)
    if note:
        return jsonify(note.to_json())
    return jsonify({'error': 'no note found'})

@notes_bp.route('/notes/<user_id>',methods=['POST'])
def create_notes(user_id):
    try:
        print(user_id)
        note = Notes.create_note(user_id,'this is my first note here')
        if note:
            print('here now')
            return jsonify({'notes': note.to_json()})

    except Exception:
        return jsonify({'notes': 'error creating notes'})

@notes_bp.route('/notes/<note_id>',methods=['DELETE'])
def delete_notes(note_id):
    note = Notes.delete_note(note_id)
    if note:
        return jsonify({'message': 'note deleted'})
    return jsonify({'error': 'note not found'})
