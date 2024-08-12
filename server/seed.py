from app import app, db
from models import User, Neighborhood, Event, News, Admin, SuperAdmin, Notification, Dashboard
from werkzeug.security import generate_password_hash
from datetime import datetime
from sqlalchemy import inspect

with app.app_context():
    db.drop_all()
    db.create_all()


    # Check if the tables are created
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    print(f"Tables in the database: {tables}")

    if 'neighborhood' in tables: 
        # Create neighborhoods
        neighborhood1 = Neighborhood(name="Downtown", description="Central business district")
        neighborhood2 = Neighborhood(name="Uptown", description="Residential area with parks")

        db.session.add_all([neighborhood1, neighborhood2])
        db.session.commit()

        # Create users
        user1 = User(
            name="John Doe",
            email="john@example.com",
            password=generate_password_hash("password123", method='sha256'),
            neighborhood_id=neighborhood1.neighborhood_id
        )
        user2 = User(
            name="Jane Smith",
            email="jane@example.com",
            password=generate_password_hash("password456", method='sha256'),
            neighborhood_id=neighborhood2.neighborhood_id
        )

        db.session.add_all([user1, user2])
        db.session.commit()

        # Create events
        event1 = Event(
            title="Community Cleanup",
            description="Join us for a neighborhood cleanup.",
            date=datetime(2024, 8, 15, 10, 0),
            location="Downtown Park",
            status="Scheduled",
            user_id=user1.user_id,
            neighborhood_id=neighborhood1.neighborhood_id
        )

        db.session.add(event1)
        db.session.commit()

        # Create news
        news1 = News(
            title="New Community Center",
            content="A new community center is opening in Uptown.",
            status="Published",
            user_id=user2.user_id,
            neighborhood_id=neighborhood2.neighborhood_id
        )

        db.session.add(news1)
        db.session.commit()

        # Create admin and super admin
        admin1 = Admin(
            user_id=user1.user_id,
            neighborhood_id=neighborhood1.neighborhood_id
        )
        super_admin1 = SuperAdmin(
            user_id=user2.user_id
        )

        db.session.add_all([admin1, super_admin1])
        db.session.commit()

        print("Database seeded successfully!")
    else:
        print("The 'neighborhood' table does not exist. Please check your database setup.")
