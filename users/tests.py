from django.test import TestCase
from django.contrib.auth import authenticate, login,logout
from .forms import Registration
from .models import User

# Create your tests here.

from django.test import Client


class SimpleTest(TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        self.form_data={
            'email':'aman@aman.aman',
            'password':'aman123456',
            'password2':'aman123456',
        }


    def test_details(self):
        # Issue a GET request.
        response = self.client.get('/login/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        # First check for the default behavior
        response = self.client.get('/profile/')
        self.assertRedirects(response, '/login/?next=/profile/')

        # Then override the LOGIN_URL setting
        with self.settings(LOGIN_URL='/login/'):

            response = self.client.get('/profile/')
            self.assertRedirects(response, '/login/?next=/profile/')




    def test_valid_data(self):
        self.form12=Registration(self.form_data)
        #import ipdb;ipdb.set_trace()
        self.assertTrue(self.form12.is_valid())



    def test_blank_data(self):
        self.form_data.update({'password':""})
        self.form1=Registration(self.form_data)
        self.assertFalse(self.form1.is_valid())
        self.assertEqual(self.form1.errors,{'__all__': ['password must have atleast 8 letter']})





from django.test import TestCase
from django.test import Client
from .forms import *   # import all forms

class Setup_Class(TestCase):

    def setUp(self):
        self.user = User.objects.create(email="user@mp.com", password="user",)

class User_Form_Test(TestCase):

    # Valid Form Data
    def test_UserForm_valid(self):
        form = Registration(data={'email': "user@mp.com", 'password': "user12345", 'password2':"user12345"})
        form.save()
        self.assertTrue(form.is_valid())

    # Invalid Form Data
    def test_UserForm_invalid(self):
        form = Registration(data={'email': "", 'password': "mp", 'password2':""})
        self.assertFalse(form.is_valid())


class User_Views_Test(Setup_Class):
    def setUp(self):
        User.objects.create_user('abc@abc.abc', 'shubham10')

    def test_home_view(self):

        user_login = self.client.login(email="abc@abc.abc", password="shubham10")
        self.assertTrue(user_login)
        response = self.client.post("/login/")
        self.assertEqual(response.status_code, 302)

    def test_add_user_view(self):
        response = self.client.get("/register/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/register.html")



    # Valid Data
    def test_add_admin_form_view(self):
        user_count = User.objects.count()
        response = self.client.post("/register/", {'email': "user@mp.com", 'password': "user12345", 'password2':"user12345"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.count(), user_count+1)
