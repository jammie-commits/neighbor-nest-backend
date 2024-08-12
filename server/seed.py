import random
from faker import Faker
from app import db, app  # Import the app
from models import User, Neighborhood, Event, News

fake = Faker()

def create_neighborhoods(num_neighborhoods=5):
    neighborhoods = []
    for _ in range(num_neighborhoods):
        neighborhood = Neighborhood(
            name=fake.city(),
            description=fake.paragraph()
        )
        db.session.add(neighborhood)
        neighborhoods.append(neighborhood)
    db.session.commit()
    return neighborhoods

def create_users(num_users=20, neighborhoods=None):
    users = []
    for _ in range(num_users):
        user = User(
            name=fake.name(),
            email=fake.unique.email(),
            password=fake.password(),
            profile_picture_url=fake.image_url(),
            neighborhood_id=random.choice(neighborhoods).neighborhood_id,
            is_admin=fake.boolean(chance_of_getting_true=20),
            is_super_admin=fake.boolean(chance_of_getting_true=5)
        )
        db.session.add(user)
        users.append(user)
    db.session.commit()
    return users

def create_events(num_events=15, users=None, neighborhoods=None):
    events = []
    for _ in range(num_events):
        event = Event(
            title=fake.sentence(),
            description=fake.paragraph(),
            date=fake.future_datetime(),
            location=fake.address(),
            image_url=fake.image_url(),
            status=random.choice(['Scheduled', 'Cancelled', 'Completed']),
            user_id=random.choice(users).user_id,
            neighborhood_id=random.choice(neighborhoods).neighborhood_id,
            admin_approved=fake.boolean(chance_of_getting_true=70)
        )
        db.session.add(event)
        events.append(event)
    db.session.commit()
    return events

def create_news(num_news=10, users=None, neighborhoods=None):
    news_list = []
    for _ in range(num_news):
        news = News(
            title=fake.sentence(),
            content=fake.paragraph(),
            image_url=fake.image_url(),
            status=random.choice(['Published', 'Draft']),
            user_id=random.choice(users).user_id,
            neighborhood_id=random.choice(neighborhoods).neighborhood_id,
            admin_approved=fake.boolean(chance_of_getting_true=70)
        )
        db.session.add(news)
        news_list.append(news)
    db.session.commit()
    return news_list

def seed_database():
    db.drop_all()
    db.create_all()

    neighborhoods = create_neighborhoods()
    users = create_users(neighborhoods=neighborhoods)
    create_events(users=users, neighborhoods=neighborhoods)
    create_news(users=users, neighborhoods=neighborhoods)

    print("Database seeded successfully!")

if __name__ == '__main__':
    with app.app_context():  
        seed_database()
