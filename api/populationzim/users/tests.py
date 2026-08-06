from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse("users:create")

def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):
    """Test public features of users api"""
    
    def setUp(self):
        self.client = APIClient()
        
    def test_create_user_success(self):
        """Test creating a user is successful"""
        
        user_data = { "email": "test-users@ravira.com",
                      "password": "raviraindezvenyu",
                      "name": "Santiago Chocobares" }
        
        response = self.client.post(CREATE_USER_URL,user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        user = get_user_model().objects.get(email=user_data["email"])
        self.assertTrue(user.check_password(user_data["password"]))
        
        self.assertNotIn("password", response.data)

    def test_user_with_email_exists_error(self):
        """Tests if email used to create new user does not exist"""
        
        def create_user(**params):
            """Create and return a new user"""
            return get_user_model().objects.create_user(**params)
        
        user_data = { "email": "test-users1@ravira.com",
                      "password": "raviraindezvenyu",
                      "name": "Santiago Chocobares" }
        
        create_user(**user_data)

        response = self.client.post(CREATE_USER_URL,user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test if error is returned when password being used to create user is too short"""
        
        user_data = { "email": "test-users1@ravira.com",
                      "password": "ravi",
                      "name": "Santiago Chocobares" }
        
        response = self.client.post(CREATE_USER_URL,user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        user_exists = get_user_model().objects.filter(email=user_data["email"]).exists()
        self.assertFalse(user_exists)

