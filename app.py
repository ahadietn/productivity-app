from config import app, db
from flask_restful import Api
from auth import Signup, Login, Logout, Me


api = Api(app)

api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(Me, '/me')

if __name__ == '__main__':
    app.run(debug=True)