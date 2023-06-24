import json
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework import status

from webapp.models import HackerNewsPost


class SignUpTestCase(APITestCase):
    '''
    Test for user registration
    '''
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            "email": "testuser@test.com",
            "username" : "testuser",
            "password": "password"
            }
        self.post_data = {
            "title": 'Test Tile',
            "text" : 'Test Text',
            "type": 'poll',
            "url": 'https://testurl.com/'
            }
        self.register_url = '/auth/register/'
        self.login_url = '/auth/login/'
        self.get_all_posts_url = '/api/all-posts/'
        self.get_one_post_url = '/api/post/{post_id}/'
        self.add_post_url = '/api/add-post/'
        self.manage_post_url = '/api/manage-post/{post_id}/'

    def signup_and_login_user(self):
        # Register a test user
        data = self.user_data.copy()
        self.client.post(self.register_url, data)

        # Login and get the test user token
        data.pop('email')
        login_response = self.client.post(self.login_url, data)
        token = login_response.data['token']['access']

        return token

    def test_get_all_posts_success(self):
        # Test retrieving all posts
        response = self.client.get(self.get_all_posts_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_one_post_through_api_success(self):
        token = self.signup_and_login_user() # register a test user and get their token
        # Add a post using the API with authentication
        response = self.client.post(self.add_post_url, self.post_data, HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_get_one_post_success(self):
        token = self.signup_and_login_user() # register a test user and get their token
        self.client.post(self.add_post_url, self.post_data, HTTP_AUTHORIZATION=f'Bearer {token}') # create a post with the test user
        post_id = HackerNewsPost.objects.first().post_id
        # Test retrieving a specific post
        response = self.client.get(self.get_one_post_url.format(post_id=post_id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_one_post_fail_post_not_found(self):
        # Test retrieving a non-existent post
        response = self.client.get(self.get_one_post_url.format(post_id=80000000))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_add_one_post_fail_invalid_data(self):
        # Attempt to add a post with invalid data
        token = self.signup_and_login_user() # register a test user and get their token
        
        # Test invalid type
        data = self.post_data.copy()
        data['type'] = 'type'
        response = self.client.post(self.add_post_url, data, HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.content, b'{"errors":["type can only be one of these choices: [\'job\', \'story\', \'poll\', \'pollopt\']"]}')

        # Test empty titleTest invalid type
        data = self.post_data.copy()
        data.pop('title')
        response = self.client.post(self.add_post_url, data, HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.content, b'{"title":["This field is required."]}')

        # Test empty text
        data = self.post_data.copy()
        data.pop('text')
        response = self.client.post(self.add_post_url, data, HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.content, b'{"text":["This field is required."]}')
    
    def test_update_post_success(self):
        token = self.signup_and_login_user() # register a test user and get their token
        self.client.post(self.add_post_url, self.post_data, HTTP_AUTHORIZATION=f'Bearer {token}') # create a post with the test user
        post_id = HackerNewsPost.objects.first().post_id # Get the created post_id
        data = self.post_data.copy()
        data['title'] = 'Updated Test Title'
        response = self.client.put(self.manage_post_url.format(post_id=post_id), data, HTTP_AUTHORIZATION=f'Bearer {token}')
        response_content = json.loads(response.content) # Convert the data to json
        title = response_content['title'] # Get the title from the response content
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(title, data['title'])
    
    def test_update_post_fail_invalid_type(self):
        token = self.signup_and_login_user() # register a test user and get their token
        self.client.post(self.add_post_url, self.post_data, HTTP_AUTHORIZATION=f'Bearer {token}') # create a post with the test user
        post_id = HackerNewsPost.objects.first().post_id # Get the created post_id
        data = self.post_data.copy()
        data['type'] = 'type'
        response = self.client.put(self.manage_post_url.format(post_id=post_id), data, HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.content, b'{"errors":["type can only be one of these choices: [\'job\', \'story\', \'poll\', \'pollopt\']"]}')
    
    def test_update_post_fail_unauthorized_user(self):
        first_user_token = self.signup_and_login_user() # register the first test user and get their token
        
        # Get and update the original data for the second test user
        user_data = self.user_data.copy()
        user_data['email'] = 'testuser2@email.com'
        user_data['username'] = 'testuser2'
        self.client.post(self.register_url, user_data) # Register the second user
        
        # Login and get the second test user token
        user_data.pop('email')
        login_response = self.client.post(self.login_url, user_data)
        second_user_token = login_response.data['token']['access']

        self.client.post(self.add_post_url, self.post_data, HTTP_AUTHORIZATION=f'Bearer {first_user_token}')
        post_id = HackerNewsPost.objects.first().post_id
        data = self.post_data.copy()
        data['title'] = 'Updated Test Title'
        response = self.client.put(self.manage_post_url.format(post_id=post_id), data, HTTP_AUTHORIZATION=f'Bearer {second_user_token}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_update_post_fail_not_found(self):
        token = self.signup_and_login_user() # register a test user and get their token
        self.client.post(self.add_post_url, self.post_data, HTTP_AUTHORIZATION=f'Bearer {token}') # create a post with the test user
        data = self.post_data.copy()
        data['title'] = 'Updated Test Title'
        response = self.client.put(self.manage_post_url.format(post_id='80000000'), data, HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_post_success(self):
        token = self.signup_and_login_user() # register a test user and get their token
        self.client.post(self.add_post_url, self.post_data, HTTP_AUTHORIZATION=f'Bearer {token}') # create a post with the test user
        post_id = HackerNewsPost.objects.first().post_id
        response = self.client.delete(self.manage_post_url.format(post_id=post_id), HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_post_fail_unauthorized_user(self):
        first_user_token = self.signup_and_login_user() # register a test user and get their token

        # Get and update the original data for the second test user
        user_data = self.user_data.copy()
        user_data['email'] = 'testuser2@email.com'
        user_data['username'] = 'testuser2'
        self.client.post(self.register_url, user_data) # register the second user
        
        # Login and get the test user token
        user_data.pop('email')
        login_response = self.client.post(self.login_url, user_data)
        second_user_token = login_response.data['token']['access']

        self.client.post(self.add_post_url, self.post_data, HTTP_AUTHORIZATION=f'Bearer {first_user_token}') # Create a post with the first test user
        post_id = HackerNewsPost.objects.first().post_id # Get the post_id
        response = self.client.delete(self.manage_post_url.format(post_id=post_id), HTTP_AUTHORIZATION=f'Bearer {second_user_token}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_post_success(self):
        token = self.signup_and_login_user() # register a test user and get their token
        self.client.post(self.add_post_url, self.post_data, HTTP_AUTHORIZATION=f'Bearer {token}') # create a post with the test user
        response = self.client.delete(self.manage_post_url.format(post_id='90000000'), HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)