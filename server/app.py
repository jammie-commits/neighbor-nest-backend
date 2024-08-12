from datetime import datetime, timedelta
from sqlite3 import IntegrityError
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_restful import Api, Resource
from models import User, Neighborhood, Event, News

app = Flask(__name__)

# JWT Configuration
# app.config["JWT_SECRET_KEY"] = "kdjhhgjdxkjfjndjbtkdnjbj4fg"
# jwt = JWTManager(app)

# Database Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///app.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# CORS and Migrations
CORS(app)
db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

class Home(Resource):
    def get(self):
        return {"message": "Welcome to Neighbornest"}, 200
    
class UserRegister(Resource):
    def post(self):
        data = request.get_json()
        hashed_password = generate_password_hash(data['password'], method='sha256')
        new_user = User(
            name=data['name'],
            email=data['email'],
            password=hashed_password,
            neighborhood_id=data.get('neighborhood_id')
        )
        try:
            db.session.add(new_user)
            db.session.commit()
            return {"message": "User registered successfully"}, 201
        except IntegrityError:
            db.session.rollback()
            return {"message": "Email already exists"}, 409

class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        if user and check_password_hash(user.password, data['password']):
            access_token = create_access_token(identity=user.user_id, expires_delta=timedelta(days=7))
            return {"token": access_token}, 200
        else:
            return {"message": "Invalid credentials"}, 401

class ProtectedResource(Resource):
    # @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        return {"message": f"Hello, {user.name}!"}, 200
    
class Users(Resource):
    # @jwt_required()
    def get(self):
        users = User.query.all()
        return [user.to_dict() for user in users], 200

class UserByID(Resource):
    # @jwt_required()
    def get(self, user_id):
        user = User.query.get(user_id)
        if user:
            return user.to_dict(), 200
        else:
            return {"message": "User not found"}, 404

    # @jwt_required()
    def put(self, user_id):
        data = request.get_json()
        user = User.query.get(user_id)
        if user:
            user.name = data.get('name', user.name)
            user.email = data.get('email', user.email)
            user.profile_picture_url = data.get('profile_picture_url', user.profile_picture_url)
            user.is_admin = data.get('is_admin', user.is_admin)
            user.is_super_admin = data.get('is_super_admin', user.is_super_admin)
            user.neighborhood_id = data.get('neighborhood_id', user.neighborhood_id)
            user.updated_at = datetime.utcnow()  # Fix: Removed quotes
            db.session.commit()
            return {"message": "User updated successfully"}, 200
        else:
            return {"message": "User not found"}, 404

    # @jwt_required()
    def delete(self, user_id):
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return {"message": "User deleted successfully"}, 200
        else:
            return {"message": "User not found"}, 404
        
class Neighborhoods(Resource):
    # @jwt_required()
    def post(self):
        data = request.get_json()
        new_neighborhood = Neighborhood(
            name=data['name'],
            description=data.get('description')
        )
        db.session.add(new_neighborhood)
        db.session.commit()
        return {"message": "Neighborhood created successfully"}, 201

    # @jwt_required()
    def get(self):
        neighborhoods = Neighborhood.query.all()
        return [neighborhood.to_dict() for neighborhood in neighborhoods], 200
    
class NeighborhoodByID(Resource):
    # @jwt_required()
    def put(self, neighborhood_id):
        data = request.get_json()
        neighborhood = Neighborhood.query.get(neighborhood_id)
        if neighborhood:
            neighborhood.name = data.get('name', neighborhood.name)
            neighborhood.description = data.get('description', neighborhood.description)
            neighborhood.updated_at = datetime.utcnow()  # Fix: Removed quotes
            db.session.commit()
            return {"message": "Neighborhood updated successfully"}, 200
        else:
            return {"message": "Neighborhood not found"}, 404

    # @jwt_required()
    def delete(self, neighborhood_id):
        neighborhood = Neighborhood.query.get(neighborhood_id)
        if neighborhood:
            db.session.delete(neighborhood)
            db.session.commit()
            return {"message": "Neighborhood deleted successfully"}, 200
        else:
            return {"message": "Neighborhood not found"}, 404
        
class Events(Resource):
    # @jwt_required()
    def post(self):
        data = request.get_json()
        new_event = Event(
            title=data['title'],
            description=data['description'],
            date=data['date'],
            location=data['location'],
            image_url=data.get('image_url'),
            status=data['status'],
            user_id=data['user_id'],
            neighborhood_id=data['neighborhood_id']
        )
        db.session.add(new_event)
        db.session.commit()
        return {"message": "Event created successfully"}, 201

    # @jwt_required()
    def get(self):
        events = Event.query.all()
        return [event.to_dict() for event in events], 200

class EventByID(Resource):
    # @jwt_required()
    def put(self, event_id):
        data = request.get_json()
        event = Event.query.get(event_id)
        if event:
            event.title = data.get('title', event.title)
            event.description = data.get('description', event.description)
            event.date = data.get('date', event.date)
            event.location = data.get('location', event.location)
            event.image_url = data.get('image_url', event.image_url)
            event.status = data.get('status', event.status)
            event.admin_approved = data.get('admin_approved', event.admin_approved)
            event.updated_at = datetime.utcnow()  # Fix: Removed quotes
            db.session.commit()
            return {"message": "Event updated successfully"}, 200
        else:
            return {"message": "Event not found"}, 404

    # @jwt_required()
    def delete(self, event_id):
        event = Event.query.get(event_id)
        if event:
            db.session.delete(event)
            db.session.commit()
            return {"message": "Event deleted successfully"}, 200
        else:
            return {"message": "Event not found"}, 404

class NewsResource(Resource):
    # @jwt_required()
    def post(self):
        data = request.get_json()
        new_news = News(
            title=data['title'],
            content=data['content'],
            image_url=data.get('image_url'),
            status=data['status'],
            user_id=data['user_id'],
            neighborhood_id=data['neighborhood_id']
        )
        db.session.add(new_news)
        db.session.commit()
        return {"message": "News created successfully"}, 201

    @jwt_required()
    def get(self):
        news_items = News.query.all()
        return [news.to_dict() for news in news_items], 200

class NewsByID(Resource):
    # @jwt_required()
    def put(self, news_id):
        data = request.get_json()
        news = News.query.get(news_id)
        if news:
            news.title = data.get('title', news.title)
            news.content = data.get('content', news.content)
            news.image_url = data.get('image_url', news.image_url)
            news.status = data.get('status', news.status)
            news.admin_approved = data.get('admin_approved', news.admin_approved)
            news.updated_at = datetime.utcnow()  # Fix: Removed quotes
            db.session.commit()
            return {"message": "News updated successfully"}, 200
        else:
            return {"message": "News not found"}, 404

    # @jwt_required()
    def delete(self, news_id):
        news = News.query.get(news_id)
        if news:
            db.session.delete(news)
            db.session.commit()
            return {"message": "News deleted successfully"}, 200
        else:
            return {"message": "News not found"}, 404

# Adding resources to the API
api.add_resource(Home, '/')
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(ProtectedResource, '/protected')
api.add_resource(Users, '/users')
api.add_resource(UserByID, '/users/<int:user_id>')
api.add_resource(Neighborhoods, '/neighborhoods')
api.add_resource(NeighborhoodByID, '/neighborhoods/<int:neighborhood_id>')
api.add_resource(Events, '/events')
api.add_resource(EventByID, '/events/<int:event_id>')
api.add_resource(NewsResource, '/news')
api.add_resource(NewsByID, '/news/<int:news_id>')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5000, debug=True)
