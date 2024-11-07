from flask import   Blueprint,g,jsonify
from app import init_session
from app.database.Users import User

users_bp = Blueprint('users_bp',__name__)


@users_bp.route('/users',methods=['GET'])
def get_users():
    # init_session()
    user = User.query.filter(User.email == 'peter@gmail.com').first()
    if user:
        print(user)
        return jsonify(user.to_json())
    return jsonify({'message': 'no user found'})

@users_bp.route('/users',methods=['POST'])
def create_users():
    init_session()
    session = g.db_session
    user = User.create_user(session,'peter','mburu','peter@gmail.com')
    print(user)
    if user:
        return jsonify({"id": user.id, "name": user.first_name, "email": user.email}), 200
    return jsonify({"message": "User not found"}), 404
    
