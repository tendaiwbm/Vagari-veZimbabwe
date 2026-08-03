from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

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

