from app import app, db
from flask_migrate import Migrate
from flask.cli import FlaskGroup
from models import User, Neighborhood, Event, News, Admin, SuperAdmin, Notification, Dashboard

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Define the CLI group
cli = FlaskGroup(app)

if __name__ == '__main__':

    cli()



