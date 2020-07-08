from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

CREATE_USER_ENDPOINT = reverse('users:signup')
TOKEN_URL = reverse('users:token')
USER_SELF_URL = reverse('users:self')


def _create_user(**params):
    return get_user_model().objects.create_user(**params)


class NonAuthenticatedUserEndpointTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_is_successful(self):
        payload = {
            'email': 'test.user@testdomain.com',
            'password': 'Password123.',
            'first_name': 'test',
            'last_name': 'user'
        }
        response = self.client.post(CREATE_USER_ENDPOINT, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**response.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', response.data)

    def test_user_exist(self):
        payload = {
            'email': 'test.user@testdomain.com',
            'password': 'Password123.',
            'first_name': 'test',
            'last_name': 'user'
        }
        _create_user(**payload)
        response = self.client.post(CREATE_USER_ENDPOINT, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        payload = {
            'email': 'test.user@testdomain.com',
            'password': 'p123',
            'name': 'test user'
        }
        response = self.client.post(CREATE_USER_ENDPOINT, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects \
            .filter(email=payload['email']) \
            .exists()
        self.assertFalse(user_exists)

    def test_create_user_token(self):
        payload = {
            'email': 'test.user@testdomain.com',
            'password': 'Password123.',
            'first_name': 'test',
            'last_name': 'user',
        }
        _create_user(**payload)
        response = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_token_invalid_credentials(self):
        _create_user(email='test22.user@testdomain.com', password='Password123.')
        payload = {
            'email': 'test22.user@testdomain.com',
            'password': 'wrong_password',
            'first_name': 'test',
            'last_name': 'user'
        }
        response = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_fails_if_user_does_not_exist(self):
        """Test user is not created if a user does not exist"""
        payload = {
            'email': 'test22.user@testdomain.com',
            'password': 'Password123.',
            'first_name': 'test',
            'last_name': 'user'
        }
        response = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_fails_if_user_submit_wrong_payload(self):
        """Test token is not generated if user payload is wrong"""
        payload = {'email': 'test22.user@testdomain.com', }
        response = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_authentication_is_required_for_user_endpoints(self):
        """Test connecting to user endpoint requires authentication"""
        response = self.client.get(USER_SELF_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedUserEndpointTests(TestCase):

    def setUp(self):
        self.user = _create_user(email='authenticate.user@testdomain.com',
                                 password='Password123.',
                                 first_name='test',
                                 last_name='user')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_authenticated_user_can_retrieve_own_profile(self):
        response = self.client.get(USER_SELF_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'email': self.user.email,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name
        })

    def test_post_requests_not_allowed_for_self_profile(self):
        response = self.client.post(USER_SELF_URL, {})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_user_profile_can_be_updated(self):
        payload = {
            'password': 'NewPassword123.',
            'first_name': 'new_test',
            'last_name': 'new_user'
        }
        response = self.client.patch(USER_SELF_URL, payload)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, payload['first_name'])
        self.assertEqual(self.user.last_name, payload['last_name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
