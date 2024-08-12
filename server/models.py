from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    profile_picture_url = db.Column(db.String(255))
    is_admin = db.Column(db.Boolean, default=False)
    is_super_admin = db.Column(db.Boolean, default=False)
    neighborhood_id = db.Column(db.Integer, db.ForeignKey('neighborhood.neighborhood_id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    neighborhood = db.relationship('Neighborhood', backref='users', lazy=True)
    posts = db.relationship('News', backref='author', lazy=True)
    events = db.relationship('Event', backref='organizer', lazy=True)
    notifications = db.relationship('Notification', backref='recipient', lazy=True)

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'profile_picture_url': self.profile_picture_url,
            'is_admin': self.is_admin,
            'is_super_admin': self.is_super_admin,
            'neighborhood_id': self.neighborhood_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }

class Neighborhood(db.Model, SerializerMixin):
    __tablename__ = 'neighborhoods'
    neighborhood_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    users = db.relationship('User', backref='neighborhood', lazy=True)
    events = db.relationship('Event', backref='neighborhood', lazy=True)
    news = db.relationship('News', backref='neighborhood', lazy=True)

    def to_dict(self):
        return {
            'neighborhood_id': self.neighborhood_id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }

class Event(db.Model, SerializerMixin):
    __tablename__ = 'events'
    event_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(255), nullable=False)
    image_url = db.Column(db.String(255))
    status = db.Column(db.String(50))
    admin_approved = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    neighborhood_id = db.Column(db.Integer, db.ForeignKey('neighborhood.neighborhood_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    neighborhood_id = db.Column(db.Integer, db.ForeignKey('neighborhoods.neighborhood_id'), nullable=False)
    admin_approved = db.Column(db.Boolean, default=False)
    
    # Relationships
    notifications = db.relationship('Notification', backref='event', lazy=True)

    def to_dict(self):
        return {
            'event_id': self.event_id,
            'title': self.title,
            'description': self.description,
            'date': self.date,
            'location': self.location,
            'image_url': self.image_url,
            'status': self.status,
            'user_id': self.user_id,
            'neighborhood_id': self.neighborhood_id,
            'admin_approved': self.admin_approved,
        }

class News(db.Model, SerializerMixin):
    __tablename__ = 'news'
    news_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255))
    status = db.Column(db.String(50))
    admin_approved = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    neighborhood_id = db.Column(db.Integer, db.ForeignKey('neighborhood.neighborhood_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    neighborhood_id = db.Column(db.Integer, db.ForeignKey('neighborhoods.neighborhood_id'), nullable=False)
    admin_approved = db.Column(db.Boolean, default=False)
    
    # Relationships
    notifications = db.relationship('Notification', backref='news', lazy=True)

    def to_dict(self):
        return {
            'news_id': self.news_id,
            'title': self.title,
            'content': self.content,
            'image_url': self.image_url,
            'status': self.status,
            'user_id': self.user_id,
            'neighborhood_id': self.neighborhood_id,
            'admin_approved': self.admin_approved,
        }

class Admin(db.Model, SerializerMixin):
    __tablename__ = 'admins'
    admin_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    neighborhood_id = db.Column(db.Integer, db.ForeignKey('neighborhood.neighborhood_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='admin', uselist=False)
    neighborhood = db.relationship('Neighborhood', backref='admins', lazy=True)

    def to_dict(self):
        return {
            'admin_id': self.admin_id,
            'user_id': self.user_id,
            'neighborhood_id': self.neighborhood_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }

class SuperAdmin(db.Model, SerializerMixin):
    __tablename__ = 'super_admins'
    super_admin_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='super_admin', uselist=False)

    def to_dict(self):
        return {
            'super_admin_id': self.super_admin_id,
            'user_id': self.user_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }

# Define the Notification model
class Notification(db.Model):
    notification_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'))
    news_id = db.Column(db.Integer, db.ForeignKey('news.news_id'))
    
    # Relationships
    user = db.relationship('User', backref='notifications')
    event = db.relationship('Event', backref='notifications')
    news = db.relationship('News', backref='notifications')

    def to_dict(self):
        return {
            'notification_id': self.notification_id,
            'content': self.content,
            'type': self.type,
            'created_at': self.created_at,
            'user_id': self.user_id,
            'event_id': self.event_id,
            'news_id': self.news_id,
        }

class Dashboard(db.Model, SerializerMixin):
    __tablename__ = 'dashboards'
    dashboard_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    data = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='dashboard', uselist=False)

    def to_dict(self):
        return {
            'dashboard_id': self.dashboard_id,
            'user_id': self.user_id,
            'created_at': self.created_at,
        }

