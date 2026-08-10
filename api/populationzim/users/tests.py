from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse("users:create")
TOKEN_URL = reverse("users:token")
ME_URL = reverse("users:me")

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

    def test_create_token_for_user(self):
        """Test generating token for valid user credentials"""

        user_data = { "email": "test-token@ravira.com",
                      "password": "raviraindezvenyu",
                      "name": "Santiago Chocobares" }
        
        create_user(**user_data)

        params = { "email": user_data["email"],
                    "password": user_data["password"] }

        response = self.client.post(TOKEN_URL,params)
        
        self.assertIn("token",response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """Test returns error if credentials invalid"""

        user_data = { "email": "test-token@ravira.com",
                      "password": "raviraindezvenyu",
                      "name": "Santiago Chocobares" }
        
        create_user(**user_data)

        params = { "email": user_data["email"],
                   "password": "wrongpassword" }
        
        response = self.client.post(TOKEN_URL,params)
        self.assertNotIn("token",response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_bad_password(self):
        """Test returns error if posted password is blank string"""

        user_data = { "email": "test-token@ravira.com",
                      "password": "" }
        
        response = self.client.post(TOKEN_URL,user_data)
        self.assertNotIn("token",response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test authentication enforced for users"""

        response = self.client.get(ME_URL)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test endpoints that require authentication"""

    def setUp(self):
        user_data = { "email": "test-setup@ravira.com",
                      "password": "raviraindezvenyu",
                      "name": "Marcel Cotzee" }
        
        self.user = create_user(**user_data)
        
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user"""

        response = self.client.get(ME_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, { "email": response.data["email"], 
                                          "name": response.data["name"] })

    def test_post_me_not_allowed(self):
        """Test POST not allowed for the me endpoint"""

        response = self.client.post(ME_URL,{})

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating profile for logged in user"""

        user_data = { "name": "Jack Willis", "password": "raviraiindezvenyu" }
        response = self.client.patch(ME_URL,user_data)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name,user_data["name"])
        self.assertTrue(self.user.check_password(user_data["password"]))
        self.assertEqual(response.status_code,status.HTTP_200_OK)

