from app import app  # Import the app object
from models import db, User, Neighborhood, Event, News
from datetime import datetime
from werkzeug.security import generate_password_hash

def seed_database():
    with app.app_context():

        # Create tables 
        db.create_all()

        # Clear existing data 
        db.session.query(User).delete()
        db.session.query(Neighborhood).delete()
        db.session.query(Event).delete()
        db.session.query(News).delete()
        db.session.commit()

        # Create neighborhoods first as users and events depend on them
        neighborhoods = [
            {
                "neighborhood_id": 1,
                "name": "Neighborhood 1",
                "description": "Description 1"
            },
            
        ]
        db.session.add_all([Neighborhood(**neighborhood) for neighborhood in neighborhoods])
        db.session.commit()

        # Create users
        users = [
            {
                "user_id": 1,
                "name": "user1",
                "email": "user1@example.com",  
                "password": generate_password_hash("password1"),  
                "profile_picture_url": "https://example.com/image1.jpg",
                "is_admin": False,
                "is_super_admin": False,
                "neighborhood_id": 1,
            },
            
        ]
        db.session.add_all([User(**user) for user in users])
        db.session.commit()

        # Create events
        events = [
            {
                "event_id": 1,
                "title": "Event 1",
                "description": "Description 1",
                "date": datetime.now(),
                "location": "Location 1",
                "image_url": "https://example.com/image1.jpg",
                "status": "Open",
                "admin_approved": True,
                "user_id": 1,
                "neighborhood_id": 1
            },
            
        ]
        db.session.add_all([Event(**event) for event in events])
        db.session.commit()

        # Create news
        news = [
            {
                "news_id": 1,
                "title": "News 1",
                "content": "Content 1",
                "image_url": "https://example.com/image1.jpg",
                "status": "Open",
                "admin_approved": True,
                "user_id": 1,
                "neighborhood_id": 1
            },
           
        ]
        db.session.add_all([News(**new) for new in news])
        db.session.commit()

if __name__ == '__main__':
    seed_database()
