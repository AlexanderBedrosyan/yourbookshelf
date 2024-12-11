# Bookshelf 📚
Bookshelf is a web application for managing books, authors, and user interactions with books. Users can add books, associate them with authors, rate them, and leave comments. Each user can also track the status of their books (e.g., Read, Currently Reading, Want to Read). There is a quiz element, which can help to learn more for the books and authors.

# Features
* Add and manage books and authors.
* Rate books and leave comments.
* Quiz
* Track the reading status of books.
* User-friendly interface built primarily with Django's standard features, including templates, forms, and views. The application also includes a small RESTful API component powered by Django REST Framework for specific functionalities.

# Installation and Setup
Follow these steps to get the project running locally:

## 1. Clone the Repository
git clone [https://github.com/yourusername/bookshelf.git](https://github.com/AlexanderBedrosyan/yourbookshelf.git)

cd bookshelf

## 2. Create a Virtual Environment
python -m venv venv

source env/bin/activate

## 3. Install Dependencies
pip install -r requirements.txt

## 4. Configure Environment Variables
Create a .env file in the project's root directory with the following variables:

`SECRET_KEY=your_secret_key`<br>
`DEBUG=True`<br>
`DB_NAME=your_database_name`<br>
`DB_USER=your_database_user`<br>
`DB_PASSWORD=your_database_password`<br>
`DB_HOST=your_database_host`<br>
`DB_PORT=your_database_port`<br>

## 5. Prepare the Database
Run the following commands to set up the database schema:

`python manage.py makemigrations`<br>
`python manage.py migrate`

## 6. Create a Superuser
Create an admin account to access the Django admin panel:

`python manage.py createsuperuser`

## 7. Start the Development Server
Run the application locally:

`python manage.py runserver`

Visit http://127.0.0.1:8000/ to explore the app.

# Admin Roles and Permissions
The project includes a role-based access control system with four distinct admin roles/groups:

* User: Limited access, typically for regular users interacting with the platform's basic features.
* Administrator: Broader access, including management of specific entities such as books and authors.
* Manager: Intermediate role with permissions to oversee user activity and moderate content.
* Superuser: Full access to all features and administrative functions within the system, including critical settings and database management.

Only the Superuser has unrestricted access to all aspects of the project. Each role is designed to ensure clear and secure delegation of responsibilities.

# Project Structure

bookshelf/<br>
├── accounts/      # Custom user model and authentication logic<br>
├── author/        # Author-related models, views, and templates<br>
├── book/          # Book-related models, views, and templates<br>
├── common/        # Shared functionality (e.g., comments, ratings)<br>
└── settings.py    # Django project settings<br>
templates/     # HTML templates<br>
static/        # Static files (CSS, JS, images)<br>
tests/

# Technical Details
## Stack
- Backend: Django 4.2, Django REST Framework
- Database: PostgreSQL
- Frontend: HTML/CSS (Django templates), JavaScript, Bootstrap

# Deployed At
[Bookshelf Live Demo](https://sakeee1926.pythonanywhere.com/)

# License
This project is licensed under the MIT License.

