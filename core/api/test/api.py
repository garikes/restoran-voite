import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from ..models import *

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
def test_register_user(api_client):
    url = reverse('register')  # Make sure you have set up the name for the RegisterAPIView URL in your Django urls.py
    data = {
        "first_name": "John",
        "last_name": "Doe",
        "username": "john_doe",
        "email": "john@example.com",
        "password": "testpassword",
        "phone": "1234567890"
    }
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_200_OK
    assert Employee.objects.count() == 1

@pytest.mark.django_db
def test_login_user(api_client):
    # Create a test user
    user = Employee.objects.create_user(
        username='testuser',
        password='testpassword',
        email='testuser@example.com'
    )

    url = reverse('login')
    data = {
        "username": "testuser",
        "password": "testpassword"
    }
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    assert "refresh" in response.data

@pytest.mark.django_db
def test_vote_for_menu(api_client):
    # Create a test user
    user = Employee.objects.create_user(
        username='testuser',
        password='testpassword',
        email='testuser@example.com'
    )

    # Create a test menu
    menu = Menu.objects.create(
        restaurant_id=1,
        file='menu.pdf',
        created_by='2023-07-29'
    )

    url = reverse('vote', args=[menu.id])
    api_client.force_authenticate(user=user)
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert Vote.objects.count() == 1
    assert menu.votes == 1
