from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from geo import models


class ModelTests(TestCase):
    """Tests for custom user model"""

    def test_create_user_with_email_successful(self):

        email = "test@ravira.com"
        password = "raviraindezvenyu"

        user = get_user_model().objects.create_user(email=email,password=password)

        self.assertEqual(user.email,email)
        self.assertTrue(user.check_password(password))
    
    def test_new_user_email_normalized(self):
         
        test_emails = [["test1@rAVIRa.com","test1@ravira.com"],
                       ["Test2@Ravira.com","Test2@ravira.com"],
                       ["TEST3@RAVIRA.COM","TEST3@ravira.com"],
                       ["test4@ravira.COM","test4@ravira.com"]]

        for given_email,accepted_format in test_emails:
            user = get_user_model().objects.create_user(given_email,"ravira345")
            self.assertEqual(user.email,accepted_format)

    def test_new_user_without_email_raises_error(self):

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("","ravira345")

    def test_create_superuser(self):
        
        user_data = { "email": "test@ravira.com",
                      "password": "ravira345" }
        
        user = get_user_model().objects.create_superuser(**user_data)

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)


from django.test import Client
from django.urls import reverse


class AdminSiteTests(TestCase):
    """Tests for Django admin"""

    def setUp(self):
        """Create user and client"""

        admin_data = { "email": "test-admin@ravira.com",
                       "password": "ravira678" }
        
        user_data = { "email": "test@ravira.com",
                      "password": "raviraindezvenyu",
                      "name": "Thomas Ramos" }
        
        self.client = Client()
        self.admin = get_user_model().objects.create_superuser(**admin_data)

        self.client.force_login(self.admin)
        self.user = get_user_model().objects.create_user(**user_data)
        

    def test_users_list(self):
        """Test that users are listed on page"""

        url = reverse("admin:geo_user_changelist")
        response = self.client.get(url)

        self.assertContains(response,self.user.name)
        self.assertContains(response,self.user.email)

    def test_edit_user_page(self):
        """Test that the edit user page works"""

        url = reverse("admin:geo_user_change",args=[self.user.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code,200)

    def test_create_user_page(self):
        """Test that the create user page works"""

        url = reverse("admin:geo_user_add")
        response = self.client.get(url)

        self.assertEqual(response.status_code,200)

    def test_create_recipe(self):
        """Test creating a recipe is successful"""

        user_data = { "email": "test-recipe@ravira.com",
                      "password": "raviraindezvenyu",
                      "name": "Finn Smith" }

        user = get_user_model().objects.create_user(**user_data)

        recipe = models.Recipe.objects.create(user=user,
                                              title="Haifiridzi",
                                              time_minutes=5,
                                              price=Decimal("1.75"),
                                              description="Mirairo yekubika haifiridzi")

        self.assertEqual(str(recipe),recipe.title)














