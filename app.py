from models import db
from flask import Flask
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_restful import Resource, Api

from resources.book import BookResource
from resources.inventory import InventoryResource
from resources.record import RecordResource
from resources.user import UserResource
from resources.user import LoginResource


app = Flask(__name__)
api = Api(app)

#initialize bcrypt
bcrypt = Bcrypt(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

migrate = Migrate(app, db)
class HelloWorld(Resource):
    def get(self):
        return {"message": "Hello World"}
    
api.add_resource(HelloWorld, '/')
api.add_resource(LoginResource, '/login')
api.add_resource(BookResource, '/books', '/book/<int:id>')
api.add_resource(InventoryResource, '/inventories', '/inventory/<int:id>')
api.add_resource(RecordResource, '/records', '/record/<int:id>')
api.add_resource(UserResource, '/users', '/user/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)

# export FLASK_APP=app.py