#!/usr/bin/env python3

# Remote library imports
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
import cloudinary.uploader

# Local imports
from config import app, db
from models import User, Event, News
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Initialize JWT
jwt = JWTManager(app)

# Initialize API
api = Api(app)

# Resources
class Register(Resource):
    def post(self):
        data = request.get_json()
        hashed_password = generate_password_hash(data['password'], method='sha256')
        new_user = User(name=data['name'], email=data['email'], password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully!'})

class Login(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        if not user or not check_password_hash(user.password, data['password']):
            return jsonify({'message': 'Invalid credentials!'})
        token = create_access_token(identity={'email': user.email})
        return jsonify({'token': token})

class EventResource(Resource):
    def post(self):
        data = request.get_json()
        image_url = ""
        if 'image' in request.files:
            image = request.files['image']
            result = cloudinary.uploader.upload(image)
            image_url = result['url']
        new_event = Event(
            title=data['title'],
            description=data['description'],
            date=data['date'],
            location=data['location'],
            image_url=image_url,
            status=data['status'],
            user_id=data['user_id'],
            neighborhood_id=data['neighborhood_id']
        )
        db.session.add(new_event)
        db.session.commit()
        return jsonify({'message': 'Event created successfully!'})

class NewsResource(Resource):
    def post(self):
        data = request.get_json()
        image_url = ""
        if 'image' in request.files:
            image = request.files['image']
            result = cloudinary.uploader.upload(image)
            image_url = result['url']
        new_news = News(
            title=data['title'],
            content=data['content'],
            image_url=image_url,
            status=data['status'],
            user_id=data['user_id'],
            neighborhood_id=data['neighborhood_id']
        )
        db.session.add(new_news)
        db.session.commit()
        return jsonify({'message': 'News created successfully!'})

class SendEmail(Resource):
    def post(self):
        data = request.get_json()
        message = Mail(
            from_email='your_email@example.com',
            to_emails=data['recipient_email'],
            subject=data['subject'],
            html_content=data['html_content']
        )
        try:
            sg = SendGridAPIClient(SENDGRID_API_KEY)
            response = sg.send(message)
            return jsonify({'message': 'Email sent successfully!'})
        except Exception as e:
            return jsonify({'message': str(e)})

# Define routes
api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(EventResource, '/events')
api.add_resource(NewsResource, '/news')
api.add_resource(SendEmail, '/send-email')

@app.route('/')
def index():
    return '<h1>Project Server</h1>'

if __name__ == '__main__':
    app.run(port=5555, debug=True)
