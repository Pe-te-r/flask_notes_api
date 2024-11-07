from flask import   Blueprint,jsonify
from app.database.Users import User

users_bp = Blueprint('users_bp',__name__)


@users_bp.route('/users',methods=['GET'])
def get_users():
    user = User.get_by_email('shakirah@gmail.com')

    if user:
        return jsonify(user.to_json())
    return jsonify({'message': 'no user found'})

@users_bp.route('/users',methods=['POST'])
def create_users():
    user = User.create_user('shakirah','muthoni','shakirah@gmail.com')
    if user:
        return jsonify({"id": user.id, "name": user.first_name, "email": user.email}), 200
    return jsonify({"message": "User not found"}), 404
    

@users_bp.route('/users/<uuid:user_id>',methods=['DELETE'])
def delete_user(user_id):
    user = User.delete_user(user_id)
    if user:
        return jsonify({'message': "User deleted"})