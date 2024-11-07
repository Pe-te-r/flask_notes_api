from flask import request,   Blueprint,jsonify
from app.database.Model import User

users_bp = Blueprint('users_bp',__name__)


@users_bp.route('/users/<user_id>',methods=['GET'])
def get_users(user_id):
    user = User.get_by_id(user_id)

    if user:
        return jsonify(user.to_json())
    return jsonify({'message': 'no user found'})

@users_bp.route('/users',methods=['POST'])
def create_users():
    data = request.json()
    if not data:
        return jsonify({'error':'no data provided'})
    
    required_fields = ['username',"first_name","last_name" ,'email', 'password']
    
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return jsonify({'error': f'Missing fields: {", ".join(missing_fields)}'}), 400
    


    user = User.create_user(data['username'],data['first_name'],data['last_name'],data['email'],data['password'])
    if user:
        return jsonify({"id": user.id, "name": user.first_name, "email": user.email}), 200
    return jsonify({"message": "User not found"}), 404
    

@users_bp.route('/users/<user_id>',methods=['DELETE'])
def delete_user(user_id):
    try:
        print('hello')
        print(user_id)
        user = User.delete_user(user_id)
        
        if user:
            return jsonify({'message': "User deleted"}),200
        
        return jsonify({'message':'user not found'}),404
    except Exception as e:
        print(f'there is an error :{e}')

        return jsonify({'error':'error deleting user'})

@users_bp.route('/users',methods=['GET'])
def getAll_users():
    try:
        users = User.get_all_users()
        if users:
            return jsonify([user.to_json() for user in users]),200
        return jsonify({'message':'no users found'}),404
    except Exception as e:
        print(f'there is an error :{e}')

@users_bp.route('/login/', methods=['POST'])
def login_user():
    pass