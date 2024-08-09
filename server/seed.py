from faker import Faker
from models import db, User, Neighborhood, Event, News
from app import app

# Create an instance of the Faker class
fake = Faker()

# Create fake data
def create_fake_data():
    with app.app_context():
        db.drop_all()
        db.create_all()

# Create fake neighborhoods
        for _ in range(5):
            neighborhood = Neighborhood(
                name=fake.city(),
                description=fake.text(max_nb_chars=200)
            )
            db.session.add(neighborhood)

        db.session.commit()
        
        
 # Create fake users
        for _ in range(10):
            user = User(
                name=fake.name(),
                email=fake.email(),
                password=fake.password(),
                neighborhood_id=fake.random_int(min=1, max=5)
            )
            db.session.add(user)

        db.session.commit()