from config import app, db
from flask_restful import Api
from auth import Signup, Login, Logout, Me
from notes import NoteList, NoteDetail

api = Api(app)

api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(Me, '/me')

# Notes routes
api.add_resource(NoteList, '/notes')
api.add_resource(NoteDetail, '/notes/<int:note_id>')

if __name__ == '__main__':
    app.run(debug=True)