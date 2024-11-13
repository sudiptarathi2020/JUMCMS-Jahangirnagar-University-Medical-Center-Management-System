from django.test import SimpleTestCase
from django.urls import reverse, resolve
from users.controllers import register, log_in, log_out


class TestUrls(SimpleTestCase):
    def test_register_url_is_resolved(self):
        url = reverse("users:users-register")
        resolved = resolve(url)
        self.assertEqual(resolved.func, register)

    def test_login_url_is_resolved(self):
        url = reverse("users:users-login")
        resolved = resolve(url)
        self.assertEqual(resolved.func, log_in)

    def test_logout_url_is_resolved(self):
        url = reverse("users:users-logout")
        resolved = resolve(url)
        self.assertEqual(resolved.func, log_out)
