#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request
from flask_restful import Resource

# Local imports
from config import app, db, api
from resources import Register, Login, EventResource, NewsResource, SendEmail

# Add your model imports
from models import User, Event, News, Neighborhood, Admin, SuperAdmin, Notification, Dashboard

# Views go here!

@app.route('/')
def index():
    return '<h1>Project Server</h1>'


if __name__ == '__main__':
    app.run(port=5555, debug=True)

