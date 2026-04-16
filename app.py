from config import app, db
from flask_restful import Api

api = Api(app)

if __name__ == '__main__':
    app.run(debug=True)