#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request
from flask_restful import Resource
from flask_jwt_extended import JWTManager, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
import cloudinary.uploader


# Local imports
from config import app, db
from models import User, Event, News
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Add your model imports
from models import User, Event, News, Neighborhood, Admin, SuperAdmin, Notification, Dashboard

# Views go here!

@app.route('/')
def index():
    return '<h1>Project Server</h1>'

# Add your routes
api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(EventResource, '/events')
api.add_resource(NewsResource, '/news')
api.add_resource(SendEmail, '/send-email')

if __name__ == '__main__':
    app.run(port=5555, debug=True)

