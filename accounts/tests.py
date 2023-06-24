from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase


class SignUpAndLoginTestCase(APITestCase):
    '''
    # This class tests user registration and login functionality
    '''
    def setUp(self):
        # Set up test data and URLs for registration and login
        self.client = APIClient()
        self.user_data = {
            "email": "testuser@test.com",
            "username" : "testuser",
            "password": "password"
            }
        self.register_url = '/auth/register/'
        self.login_url = '/auth/login/'

    '''Registration Tests'''
    
    def test_register_success(self):
        # Test successful user registration
        data = self.user_data.copy()
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_register_fail_invalid_email(self):
        # Test user registration with an invalid email
        data = self.user_data
        data['email'] = 'testuser'
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_register_fail_email_already_exists(self):
        # Test user registration with an email that already exists
        data = self.user_data
        self.client.post(self.register_url, data)
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.content, b'{"errors":["Email already exists!"]}')
    
    def test_register_fail_username_numeric_value(self):
        # Test user registration with a numeric username
        data = self.user_data
        data['username'] = '12345678'
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.content, b'{"errors":["Username must not be a numeric value"]}')
    
    def test_register_fail_username_already_exists(self):
        # Test user registration with a username that already exists
        data = self.user_data
        self.client.post(self.register_url, data)
        data['email'] = 'testuser2@test.com'
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.content, b'{"errors":["Username already exists!"]}')
    
    def test_user_register_fail_username_too_short(self):
        # Test user registration with a username that is too short
        data = self.user_data
        data['username'] = 'ab'
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.content, b'{"errors":["Username must be greater than four characters"]}')
    
    def test_user_register_fail_password_too_short(self):
        # Test user registration with a password that is too short
        data = self.user_data
        data['password'] = 'ab'
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.content, b'{"password":["Ensure this field has at least 8 characters."]}')
    
    '''Login Tests'''
    def test_login_success(self):
        # Test successful user login
        data = self.user_data
        self.client.post(self.register_url, data) # Register test user
        data.pop('email')
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_fail_invalid_username(self):
        # Test user login with an invalid username
        data = self.user_data
        self.client.post(self.register_url, data) # Register test user
        data.pop('email')
        data['username'] = 'testuser2'
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_login_fail_invalid_password(self):
        # Test user login with an invalid password
        data = self.user_data
        self.client.post(self.register_url, data) # Register test user
        data.pop('email')
        data['password'] = 'invalid'
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)