from datetime import datetime, timedelta
from sqlite3 import IntegrityError
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity 
from flask_restful import Api, Resource
from models import db, User, Neighborhood, Event, News, Admin, SuperAdmin, Notification, Dashboard

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'

db.init_app(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)
api = Api(app)

class Home(Resource):
    def get(self):
        return jsonify({"message": "Welcome to Neighbornest"}), 200
    
# User Registration
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
            return jsonify({"message": "User registered successfully"}), 201
        except IntegrityError:
            db.session.rollback()
            return jsonify({"message": "Email already exists"}), 409

# User Login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=user.user_id, expires_delta=timedelta(days=7))
        return jsonify({"token": access_token}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

# Protected route example
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    return jsonify({"message": f"Hello, {user.name}!"}), 200

# Get all users (admin only)
@app.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200

# Get user by ID
@app.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify(user.to_dict()), 200
    else:
        return jsonify({"message": "User not found"}), 404

# Update user by ID
@app.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    data = request.get_json()
    user = User.query.get(user_id)
    if user:
        user.name = data.get('name', user.name)
        user.email = data.get('email', user.email)
        user.profile_picture_url = data.get('profile_picture_url', user.profile_picture_url)
        user.is_admin = data.get('is_admin', user.is_admin)
        user.is_super_admin = data.get('is_super_admin', user.is_super_admin)
        user.neighborhood_id = data.get('neighborhood_id', user.neighborhood_id)
        user.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify({"message": "User updated successfully"}), 200
    else:
        return jsonify({"message": "User not found"}), 404

# Delete user by ID
@app.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"}), 200
    else:
        return jsonify({"message": "User not found"}), 404

# Create a neighborhood
@app.route('/neighborhoods', methods=['POST'])
@jwt_required()
def create_neighborhood():
    data = request.get_json()
    new_neighborhood = Neighborhood(
        name=data['name'],
        description=data.get('description')
    )
    db.session.add(new_neighborhood)
    db.session.commit()
    return jsonify({"message": "Neighborhood created successfully"}), 201

# Get all neighborhoods
@app.route('/neighborhoods', methods=['GET'])
@jwt_required()
def get_neighborhoods():
    neighborhoods = Neighborhood.query.all()
    return jsonify([neighborhood.to_dict() for neighborhood in neighborhoods]), 200

# Update neighborhood by ID
@app.route('/neighborhoods/<int:neighborhood_id>', methods=['PUT'])
@jwt_required()
def update_neighborhood(neighborhood_id):
    data = request.get_json()
    neighborhood = Neighborhood.query.get(neighborhood_id)
    if neighborhood:
        neighborhood.name = data.get('name', neighborhood.name)
        neighborhood.description = data.get('description', neighborhood.description)
        neighborhood.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify({"message": "Neighborhood updated successfully"}), 200
    else:
        return jsonify({"message": "Neighborhood not found"}), 404

# Delete neighborhood by ID
@app.route('/neighborhoods/<int:neighborhood_id>', methods=['DELETE'])
@jwt_required()
def delete_neighborhood(neighborhood_id):
    neighborhood = Neighborhood.query.get(neighborhood_id)
    if neighborhood:
        db.session.delete(neighborhood)
        db.session.commit()
        return jsonify({"message": "Neighborhood deleted successfully"}), 200
    else:
        return jsonify({"message": "Neighborhood not found"}), 404

# Create an event
@app.route('/events', methods=['POST'])
@jwt_required()
def create_event():
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
    return jsonify({"message": "Event created successfully"}), 201

# Get all events
@app.route('/events', methods=['GET'])
@jwt_required()
def get_events():
    events = Event.query.all()
    return jsonify([event.to_dict() for event in events]), 200

# Update event by ID
@app.route('/events/<int:event_id>', methods=['PUT'])
@jwt_required()
def update_event(event_id):
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
        event.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify({"message": "Event updated successfully"}), 200
    else:
        return jsonify({"message": "Event not found"}), 404

# Delete event by ID
@app.route('/events/<int:event_id>', methods=['DELETE'])
@jwt_required()
def delete_event(event_id):
    event = Event.query.get(event_id)
    if event:
        db.session.delete(event)
        db.session.commit()
        return jsonify({"message": "Event deleted successfully"}), 200
    else:
        return jsonify({"message": "Event not found"}), 404

# Create news
@app.route('/news', methods=['POST'])
@jwt_required()
def create_news():
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
    return jsonify({"message": "News created successfully"}), 201

# Get all news
@app.route('/news', methods=['GET'])
@jwt_required()
def get_news():
    news_items = News.query.all()
    return jsonify([news.to_dict() for news in news_items]), 200

# Update news by ID
@app.route('/news/<int:news_id>', methods=['PUT'])
@jwt_required()
def update_news(news_id):
    data = request.get_json()
    news = News.query.get(news_id)
    if news:
        news.title = data.get('title', news.title)
        news.content = data.get('content', news.content)
        news.image_url = data.get('image_url', news.image_url)
        news.status = data.get('status', news.status)
        news.admin_approved = data.get('admin_approved', news.admin_approved)
        news.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify({"message": "News updated successfully"}), 200
    else:
        return jsonify({"message": "News not found"}), 404

# Delete news by ID
@app.route('/news/<int:news_id>', methods=['DELETE'])
@jwt_required()
def delete_news(news_id):
    news = News.query.get(news_id)
    if news:
        db.session.delete(news)
        db.session.commit()
        return jsonify({"message": "News deleted successfully"}), 200
    else:
        return jsonify({"message": "News not found"}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5000, debug=True)