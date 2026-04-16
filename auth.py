from flask import session, request
from flask_restful import Resource
from models import User
from config import db

class Signup(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return {'error': 'Username and password required'}, 422

        if User.query.filter_by(username=username).first():
            return {'error': 'Username already taken'}, 422

        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        session['user_id'] = user.id
        return user.to_dict(), 201


class Login(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(username=data.get('username')).first()

        if not user or not user.check_password(data.get('password', '')):
            return {'error': 'Invalid credentials'}, 401

        session['user_id'] = user.id
        return user.to_dict(), 200


class Logout(Resource):
    def delete(self):
        session.pop('user_id', None)
        return {}, 204


class Me(Resource):
    def get(self):
        user_id = session.get('user_id')
        if not user_id:
            return {'error': 'Not authenticated'}, 401

        user = User.query.get(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        return user.to_dict(), 200