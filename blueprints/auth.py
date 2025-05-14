from flask import Blueprint, request, jsonify, session
from flask_login import logout_user, login_required
from ..models.base import db
from ..models.user import User


authbp = Blueprint('Auth', __name__, url_prefix="auth")


@authbp.route('/login', methods=['POST'])
def login():
    name = request.form['name']
    password = request.form['password']
    user = db.session.get(User, name)
    if user.verify_password(password):
        session['name'] = name
        session['role'] = user.role
        session['id'] = user.id
        return jsonify({'login': 'success'})
    return jsonify({'login': 'fail'})


@authbp.route('/logout', methods=['GET'])
@login_required
def logout():
    try:
        logout_user()
    except Exception as e:
        return jsonify({'error', str(e)}), 500
