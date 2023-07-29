build the images and run the containers:
docker-compose up -d --build

Create migrations and apply them into database. NOTE the containers must be running:

$ docker-compose exec web python manage.py makemigrations $ docker-compose exec web python manage.py migrate

Request GET /api/results/

curl -H "Authorization: Bearer <your_token>" -H "Content-Type: application/json" https://localhost:8000/api/results/


## Features

- View available menu items with different categories.
- Add items to the cart and manage orders.
- Make online payments using various payment methods.
- View order history.

## Requirements

- Python 3.6 or higher
- Django 3.0 or higher
- Web browser (recommended: Google Chrome, Mozilla Firefox)

## Setup Instructions

1. Clone the repository:

git clone https://github.com/garikes/restoran-voite.git
Install the required dependencies:
pip install -r requirements.txt

Apply migrations:
python manage.py migrate
Run the local server:
python manage.py runserver

API Endpoints
Register User: /api/v1/register/
Login User: /api/v1/login/
Logout User: /api/v1/logout/
View Restaurant Details: /api/v1/restoran/
Create/Update Restaurant: /api/v1/restoran/<int:pk>/
View Menu for Restaurant: /api/v1/restoran/<int:pk>/menu/
Create/Update Menu for Restaurant: /api/v1/restoran/<int:pk>/menu/<str:deta>
Vote for Menu: /api/v1/vote/<int:menu_id>
View Results: /api/v1/results/
Token Obtain: /api/v1/token/
Token Refresh: /api/v1/token/refresh/
Token Verify: /api/v1/token/verify/
User Authentication (djoser): /api/v1/auth/
User Authentication (djoser token): /auth/
