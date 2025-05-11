from flask import Blueprint, request, jsonify
from ..models.base import db
from ..models.user import User
from werkzeug.security import generate_password_hash


userbp = Blueprint('User', __name__)


@userbp.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        if user_id is None or user_id <= 0:
            raise ValueError("No id provided")
        user = db.session.get(User, user_id)
        if not user:
            raise ValueError('No user found')
        return jsonify(user), 200
    except Exception as e:
        return jsonify({'error': str(e)})


@userbp.route('/users', methods=['GET'])
def get_users():
    try:
        return jsonify(db.session.query(User).all()), 200
    except Exception as e:
        return jsonify({'error', str(e)}), 500


@userbp.route('/users', methods=['POST'])
def create_user():
    try:
        data = {
                'email': request.json['email'],
                'password': generate_password_hash(request.json['password'],
                                                   'sha256'),
                'role': request.json['role'],
                'name': request.json.get('name')
                }
        new_user = User(**data)
        result = db.session.add(new_user)
        db.session.commit()
        return jsonify({'newUser': result}), 201
    except Exception as e:
        return jsonify({'error', str(e)})


@userbp.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        if user_id is None or user_id <= 0:
            raise ValueError("No id provided")
        user = db.session.get(User, user_id)
        if not user:
            raise ValueError('No user found')
        update_data = {
            key: request.form.get(key)
            for key in ['name',
                        'email',
                        'password',
                        'role',
                        ]
            if request.form.get(key)
                }
        for key, value in update_data.items():
            setattr(user, key, value)
        db.session.commit()
        return jsonify({'updated': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)})


@userbp.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        if user_id is None or user_id <= 0:
            raise ValueError("No id provided")
        user = db.session.get(User, user_id)
        if not user:
            raise ValueError('No user found')
        result = db.session.delete(user)
        db.session.commit()
        return jsonify({'result': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
