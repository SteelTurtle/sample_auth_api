from django.contrib.auth import get_user_model
from django.test import TestCase


class ModuleTests(TestCase):
    def test_can_create_user_with_email(self):
        email = 'test.user@testdomain.com'
        password = 'Password123.'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_address_is_normalised(self):
        email = 'test.user@NORMALISED-TEXT.cOM'
        password = 'Password123.'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email.lower())

    def test_cannot_create_user_with_invalid_email(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email=None, password='Password123.')

    def can_create_new_superuser(self):
        user = get_user_model().objects.create_superuser(email='admin@testdomain.com',
                                                         password='Password123.')
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
