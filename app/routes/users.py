from flask import Blueprint

users_bp = Blueprint('users_bp',__name__)


@users_bp.route('/users',methods=['GET'])
def get_users():
    pass