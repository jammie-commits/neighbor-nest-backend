# Neighbourhood Community App

This is a Neighbourhood Community application built with Flask, SQLAlchemy, and JSON Server. The app allows users to register, log in, and interact with various community features such as events, news, and notifications. Administrators and SuperAdmins have additional privileges for managing neighborhoods and users.

## Features

- **User Authentication**: Secure user registration and login with JWT authentication.
- **Neighborhood Management**: Admins and SuperAdmins can create, edit, and delete neighborhoods.
- **Event Management**: Users can create, view, edit, and delete events within their neighborhood.
- **News and Notifications**: Users can stay updated with the latest news and receive notifications.
- **Admin Roles**: Different roles with varying levels of access, including User, Admin, and SuperAdmin.
- **Dashboard**: A personalized dashboard displaying user activity, submissions, and community updates.

## Technologies Used

- **Backend**: Flask, SQLAlchemy, Flask-JWT-Extended
- **Frontend**: React (optional, depending on your setup)
- **Database**: SQLite (or other databases supported by SQLAlchemy)
- **JSON Server**: Used for simulating a REST API during development and testing

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/neighborhood-community-app.git
   cd neighborhood-community-app
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database:**
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

5. **Seed the database:**
   ```bash
   python seed.py
   ```

6. **Run the Flask app:**
   ```bash
   flask run
   ```

7. **Start the JSON Server:**
   ```bash
   json-server --watch db.json --port 5001
   ```

8. **Open the app in your browser:**
   ```
   http://localhost:5000
   ```

## API Endpoints

The following API endpoints are available:

- `POST /register`: Register a new user.
- `POST /login`: Authenticate a user and return a JWT.
- `GET /neighborhoods`: Retrieve a list of neighborhoods.
- `POST /neighborhoods`: Create a new neighborhood (Admin only).
- `GET /events`: Retrieve a list of events.
- `POST /events`: Create a new event.
- `GET /news`: Retrieve the latest news.
- `POST /news`: Create a new news article (Admin only).

## Usage

- **User Registration**: Sign up using the registration form. A JWT token will be generated upon successful registration.
- **Login**: Log in with your credentials to receive a JWT token.
- **Dashboard**: Access the dashboard to view your activity, submissions, and community updates.
- **Manage Neighborhoods**: Admins and SuperAdmins can create, edit, and delete neighborhoods.
- **Manage Events and News**: Users can create and manage events, while Admins can also manage news.

## Contributing

Feel free to fork this project and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

For any questions or suggestions, feel free to reach out to us via:

**Email:** gathsam3446@gmail.com
**GitHub:** [SGathuku](https://github.com/SGathuku)

**Email:** arnoldkiprono3@gmail.com
**GitHub:** [Tunchihill](https://github.com/Tunchihill)

**Email:** gzomandi07@gmail.com
**GitHub:** [GiftZawadi](https://github.com/GiftZawadi)

**Email:** jay.mbugua.ph@gmail.com
**GitHub:** (https://github.com/jammie-commits))

**Email:** princess.mumbi@student.moringaschool.com
**GitHub:** https://github.com/cessaneh
