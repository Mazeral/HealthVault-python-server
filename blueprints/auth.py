from flask import Blueprint, request, jsonify, session
from flask_login import login_user, logout_user, login_required
from ..models.base import db
from ..models.user import User


authbp = Blueprint('Auth', __name__, url_prefix="auth")


@authbp.route('/login', methods=['POST'])
def login():
    try:
        name = request.form['name']
        # TODO: hashing
        password = request.form['password']
        user = db.session.get(User, name)
        if user.password == password:  # TODO: make sure it uses a checking method
            session['name'] = name
            session['role'] = user.role
            return jsonify({'login': 'success'})
    except Exception as e:
        return jsonify({'login': 'fail'})


@authbp.route('/logout', methods=['GET'])
def logout():
    try:
        session.pop('user', None)
        session.pop('role', None)
    except Exception as e:
        return jsonify({'error', str(e)}), 500
