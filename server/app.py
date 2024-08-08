from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from config import db
from models import User, Neighborhood, Event, News, Admin, SuperAdmin, Notification, Dashboard

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# User Routes
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    
    new_user = User(
        name=data['name'],
        email=data['email'],
        password=hashed_password,
        profile_picture_url=data.get('profile_picture_url'),
        is_admin=data.get('is_admin', False),
        is_super_admin=data.get('is_super_admin', False),
        neighborhood_id=data.get('neighborhood_id'),
    )
    
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.to_dict()), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Email already exists."}), 409

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    return jsonify(user.to_dict()), 200

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    data = request.get_json()
    if 'password' in data:
        data['password'] = generate_password_hash(data['password'], method='sha256')

    for key, value in data.items():
        setattr(user, key, value)
    
    db.session.commit()
    return jsonify(user.to_dict()), 200

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"}), 200

# Neighborhood Routes
@app.route('/neighborhoods', methods=['POST'])
def create_neighborhood():
    data = request.get_json()
    new_neighborhood = Neighborhood(
        name=data['name'],
        description=data.get('description'),
    )
    
    db.session.add(new_neighborhood)
    db.session.commit()
    return jsonify(new_neighborhood.to_dict()), 201

@app.route('/neighborhoods/<int:neighborhood_id>', methods=['GET'])
def get_neighborhood(neighborhood_id):
    neighborhood = Neighborhood.query.get(neighborhood_id)
    if not neighborhood:
        return jsonify({"message": "Neighborhood not found"}), 404
    return jsonify(neighborhood.to_dict()), 200

@app.route('/neighborhoods/<int:neighborhood_id>', methods=['PUT'])
def update_neighborhood(neighborhood_id):
    neighborhood = Neighborhood.query.get(neighborhood_id)
    if not neighborhood:
        return jsonify({"message": "Neighborhood not found"}), 404

    data = request.get_json()
    for key, value in data.items():
        setattr(neighborhood, key, value)
    
    db.session.commit()
    return jsonify(neighborhood.to_dict()), 200

@app.route('/neighborhoods/<int:neighborhood_id>', methods=['DELETE'])
def delete_neighborhood(neighborhood_id):
    neighborhood = Neighborhood.query.get(neighborhood_id)
    if not neighborhood:
        return jsonify({"message": "Neighborhood not found"}), 404
    
    db.session.delete(neighborhood)
    db.session.commit()
    return jsonify({"message": "Neighborhood deleted"}), 200

# Event Routes
@app.route('/events', methods=['POST'])
def create_event():
    data = request.get_json()
    new_event = Event(
        title=data['title'],
        description=data['description'],
        date=datetime.strptime(data['date'], '%Y-%m-%d %H:%M:%S'),
        location=data['location'],
        image_url=data.get('image_url'),
        status=data['status'],
        user_id=data['user_id'],
        neighborhood_id=data['neighborhood_id'],
        admin_approved=data.get('admin_approved', False),
    )
    
    db.session.add(new_event)
    db.session.commit()
    return jsonify(new_event.to_dict()), 201

@app.route('/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    event = Event.query.get(event_id)
    if not event:
        return jsonify({"message": "Event not found"}), 404
    return jsonify(event.to_dict()), 200

@app.route('/events/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    event = Event.query.get(event_id)
    if not event:
        return jsonify({"message": "Event not found"}), 404

    data = request.get_json()
    for key, value in data.items():
        setattr(event, key, value)
    
    db.session.commit()
    return jsonify(event.to_dict()), 200

@app.route('/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    event = Event.query.get(event_id)
    if not event:
        return jsonify({"message": "Event not found"}), 404
    
    db.session.delete(event)
    db.session.commit()
    return jsonify({"message": "Event deleted"}), 200

# News Routes
@app.route('/news', methods=['POST'])
def create_news():
    data = request.get_json()
    new_news = News(
        title=data['title'],
        content=data['content'],
        image_url=data.get('image_url'),
        status=data['status'],
        user_id=data['user_id'],
        neighborhood_id=data['neighborhood_id'],
        admin_approved=data.get('admin_approved', False),
    )
    
    db.session.add(new_news)
    db.session.commit()
    return jsonify(new_news.to_dict()), 201

@app.route('/news/<int:news_id>', methods=['GET'])
def get_news(news_id):
    news = News.query.get(news_id)
    if not news:
        return jsonify({"message": "News not found"}), 404
    return jsonify(news.to_dict()), 200

@app.route('/news/<int:news_id>', methods=['PUT'])
def update_news(news_id):
    news = News.query.get(news_id)
    if not news:
        return jsonify({"message": "News not found"}), 404

    data = request.get_json()
    for key, value in data.items():
        setattr(news, key, value)
    
    db.session.commit()
    return jsonify(news.to_dict()), 200

@app.route('/news/<int:news_id>', methods=['DELETE'])
def delete_news(news_id):
    news = News.query.get(news_id)
    if not news:
        return jsonify({"message": "News not found"}), 404
    
    db.session.delete(news)
    db.session.commit()
    return jsonify({"message": "News deleted"}), 200

# Notification Routes
@app.route('/notifications', methods=['POST'])
def create_notification():
    data = request.get_json()
    new_notification = Notification(
        content=data['content'],
        type=data['type'],
        user_id=data['user_id'],
        event_id=data.get('event_id'),
        news_id=data.get('news_id'),
    )
    
    db.session.add(new_notification)
    db.session.commit()
    return jsonify(new_notification.to_dict()), 201

@app.route('/notifications/<int:notification_id>', methods=['GET'])
def get_notification(notification_id):
    notification = Notification.query.get(notification_id)
    if not notification:
        return jsonify({"message": "Notification not found"}), 404
    return jsonify(notification.to_dict()), 200

@app.route('/notifications/<int:notification_id>', methods=['DELETE'])
def delete_notification(notification_id):
    notification = Notification.query.get(notification_id)
    if not notification:
        return jsonify({"message": "Notification not found"}), 404
    
    db.session.delete(notification)
    db.session.commit()
    return jsonify({"message": "Notification deleted"}), 200

# Admin Routes
@app.route('/admins', methods=['POST'])
def create_admin():
    data = request.get_json()
    new_admin = Admin(
        user_id=data['user_id'],
        neighborhood_id=data['neighborhood_id'],
    )
    
    db.session.add(new_admin)
    db.session.commit()
    return jsonify(new_admin.to_dict()), 201

@app.route('/admins/<int:admin_id>', methods=['GET'])
def get_admin(admin_id):
    admin = Admin.query.get(admin_id)
    if not admin:
        return jsonify({"message": "Admin not found"}), 404
    return jsonify(admin.to_dict()), 200

@app.route('/admins/<int:admin_id>', methods=['PUT'])
def update_admin(admin_id):
    admin = Admin.query.get(admin_id)
    if not admin:
        return jsonify({"message": "Admin not found"}), 404

    data = request.get_json()
    for key, value in data.items():
        setattr(admin, key, value)
    
    db.session.commit()
    return jsonify(admin.to_dict()), 200

@app.route('/admins/<int:admin_id>', methods=['DELETE'])
def delete_admin(admin_id):
    admin = Admin.query.get(admin_id)
    if not admin:
        return jsonify({"message": "Admin not found"}), 404
    
    db.session.delete(admin)
    db.session.commit()
    return jsonify({"message": "Admin deleted"}), 200

# SuperAdmin Routes
@app.route('/super_admins', methods=['POST'])
def create_super_admin():
    data = request.get_json()
    new_super_admin = SuperAdmin(
        user_id=data['user_id'],
    )
    
    db.session.add(new_super_admin)
    db.session.commit()
    return jsonify(new_super_admin.to_dict()), 201

@app.route('/super_admins/<int:super_admin_id>', methods=['GET'])
def get_super_admin(super_admin_id):
    super_admin = SuperAdmin.query.get(super_admin_id)
    if not super_admin:
        return jsonify({"message": "SuperAdmin not found"}), 404
    return jsonify(super_admin.to_dict()), 200

@app.route('/super_admins/<int:super_admin_id>', methods=['PUT'])
def update_super_admin(super_admin_id):
    super_admin = SuperAdmin.query.get(super_admin_id)
    if not super_admin:
        return jsonify({"message": "SuperAdmin not found"}), 404

    data = request.get_json()
    for key, value in data.items():
        setattr(super_admin, key, value)
    
    db.session.commit()
    return jsonify(super_admin.to_dict()), 200

@app.route('/super_admins/<int:super_admin_id>', methods=['DELETE'])
def delete_super_admin(super_admin_id):
    super_admin = SuperAdmin.query.get(super_admin_id)
    if not super_admin:
        return jsonify({"message": "SuperAdmin not found"}), 404
    
    db.session.delete(super_admin)
    db.session.commit()
    return jsonify({"message": "SuperAdmin deleted"}), 200

# Dashboard Routes
@app.route('/dashboards', methods=['POST'])
def create_dashboard():
    data = request.get_json()
    new_dashboard = Dashboard(
        user_id=data['user_id'],
    )
    
    db.session.add(new_dashboard)
    db.session.commit()
    return jsonify(new_dashboard.to_dict()), 201

@app.route('/dashboards/<int:dashboard_id>', methods=['GET'])
def get_dashboard(dashboard_id):
    dashboard = Dashboard.query.get(dashboard_id)
    if not dashboard:
        return jsonify({"message": "Dashboard not found"}), 404
    return jsonify(dashboard.to_dict()), 200

@app.route('/dashboards/<int:dashboard_id>', methods=['DELETE'])
def delete_dashboard(dashboard_id):
    dashboard = Dashboard.query.get(dashboard_id)
    if not dashboard:
        return jsonify({"message": "Dashboard not found"}), 404
    
    db.session.delete(dashboard)
    db.session.commit()
    return jsonify({"message": "Dashboard deleted"}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
