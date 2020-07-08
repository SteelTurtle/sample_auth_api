from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='supreme.admin@testdomain.com',
            password='Password123.'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='unprivileged.user@testdomain.com',
            password='Password123.',
            name='Mr. Unprivileged User'
        )

    def test_users_can_be_listed(self):
        url = reverse('admin:main_user_changelist')
        response = self.client.get(url)

        self.assertContains(response, self.user.name)
        self.assertContains(response, self.user.email)

    def test_user_change_page_renders_correctly(self):
        url = reverse('admin:main_user_change', args=[self.user.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_admin_can_create_user_page(self):
        url = reverse('admin:main_user_add')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
