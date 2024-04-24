from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from django.utils.timezone import now
from rest_framework import status
from django.urls import reverse

User = get_user_model()

class AuthenticationTests(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('token_obtain_pair')
        self.refresh_token_url = reverse('token_refresh')

        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword',
            'user_type': 'student'
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_register_user(self):
        unique_username = f'testuser_{now().timestamp()}'  # Append timestamp to make the username unique
        user_data = self.user_data.copy()
        user_data['username'] = unique_username

        response = self.client.post(self.register_url, user_data, format='json')
        print(response.content)  # Print response content for debugging
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_user(self):
        response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'testpassword'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)
        self.assertTrue('refresh' in response.data)

    def test_refresh_token(self):
        response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'testpassword'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        refresh_token = response.data['refresh']

        response = self.client.post(self.refresh_token_url, {'refresh': refresh_token}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)
