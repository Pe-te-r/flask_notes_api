from flask import jsonify, Blueprint
from app.database.Model import Notes


notes_bp = Blueprint('notes_bp',__name__)

@notes_bp.route('/notes', methods=['GET'])
def get_notes():
    # implement logic to fetch all notes from the database
    notes = Notes.get_all_notes()
    if notes:
        return jsonify({'notes': [note.to_json() for note in notes]})
    return jsonify({'error': 'no notes found'})

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
