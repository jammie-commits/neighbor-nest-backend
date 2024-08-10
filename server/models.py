from flask import Flask, request, jsonify

from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # Update with your database URI
db = SQLAlchemy(app)

# Models 
class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    profile_picture_url = db.Column(db.String(255))
    is_admin = db.Column(db.Boolean, default=False)
    is_super_admin = db.Column(db.Boolean, default=False)
    neighborhood_id = db.Column(db.Integer, db.ForeignKey('neighborhoods.neighborhood_id'))
    created_at = db.Column(db.DateTime, default=datetime)
    updated_at = db.Column(db.DateTime, default=datetime, onupdate=datetime)
    
    # Relationships
    neighborhood = db.relationship('Neighborhood', backref='users', lazy=True)
    posts = db.relationship('News', backref='author', lazy=True)
    events = db.relationship('Event', backref='organizer', lazy=True)
    notifications = db.relationship('Notification', backref='recipient', lazy=True)

class Neighborhood(db.Model, SerializerMixin):
    __tablename__ = 'neighborhoods'
    neighborhood_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime)
    updated_at = db.Column(db.DateTime, default=datetime, onupdate=datetime)
    
    # Relationships
    users = db.relationship('User', backref='neighborhood', lazy=True)
    events = db.relationship('Event', backref='neighborhood', lazy=True)
    news = db.relationship('News', backref='neighborhood', lazy=True)

class Event(db.Model, SerializerMixin):
    __tablename__ = 'events'
    event_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    image_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime)
    updated_at = db.Column(db.DateTime, default=datetime, onupdate=datetime)
    status = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    neighborhood_id = db.Column(db.Integer, db.ForeignKey('neighborhoods.neighborhood_id'), nullable=False)
    admin_approved = db.Column(db.Boolean, default=False)
    
    # Relationships
    notifications = db.relationship('Notification', backref='event', lazy=True)

class News(db.Model, SerializerMixin):
    __tablename__ = 'news'
    news_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime)
    updated_at = db.Column(db.DateTime, default=datetime, onupdate=datetime)
    status = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    neighborhood_id = db.Column(db.Integer, db.ForeignKey('neighborhoods.neighborhood_id'), nullable=False)
    admin_approved = db.Column(db.Boolean, default=False)
    
    # Relationships
    notifications = db.relationship('Notification', backref='news', lazy=True)

class Admin(db.Model, SerializerMixin):
    __tablename__ = 'admins'
    admin_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), unique=True, nullable=False)
    neighborhood_id = db.Column(db.Integer, db.ForeignKey('neighborhoods.neighborhood_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime)
    updated_at = db.Column(db.DateTime, default=datetime, onupdate=datetime)
    
    # Relationships
    user = db.relationship('User', backref='admin', uselist=False)
    neighborhood = db.relationship('Neighborhood', backref='admins', lazy=True)

class SuperAdmin(db.Model, SerializerMixin):
    __tablename__ = 'super_admins'
    super_admin_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime)
    updated_at = db.Column(db.DateTime, default=datetime, onupdate=datetime)
    
    # Relationships
    user = db.relationship('User', backref='super_admin', uselist=False)

class Notification(db.Model, SerializerMixin):
    __tablename__ = 'notifications'
    notification_id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'))
    news_id = db.Column(db.Integer, db.ForeignKey('news.news_id'))
    
    # Relationships
    user = db.relationship('User', backref='notifications')
    event = db.relationship('Event', backref='notifications')
    news = db.relationship('News', backref='notifications')

class Dashboard(db.Model, SerializerMixin):
    __tablename__ = 'dashboards'
    dashboard_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime)
    
    # Relationships
    user = db.relationship('User', backref='dashboard', uselist=False)
    
    