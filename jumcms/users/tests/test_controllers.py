from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib import messages

User = get_user_model()


class UserViewsTest(TestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            email="testuser@example.com",
            name="Test User",
            role="Patient",
            blood_group="A+",
            date_of_birth="2000-01-01",
            gender="Male",
            phone_number="+8801234567890",
            password="testpassword123",
        )
        self.user.is_approved = True
        self.user.save()

    def test_home_view(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/home.htm")

    def test_register_view_valid(self):
        response = self.client.post(
            reverse("users-register"),
            {
                "email": "newuser@example.com",
                "name": "New User",
                "role": "Doctor",
                "blood_group": "B+",
                "date_of_birth": "1995-05-05",
                "gender": "Female",
                "phone_number": "+8801987654321",
                "password": "newpassword123",
                "password_confirm": "newpassword123",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(email="newuser@example.com").exists())
        self.assertTemplateUsed(response, "users/unapproved.html")
        self.assertIn(
            "Registration successfull! Please wait unitll your account is approved!!",
            [m.message for m in messages.get_messages(response.wsgi_request)],
        )

    def test_register_view_invalid(self):
        response = self.client.post(
            reverse("users-register"),
            {
                "email": "",
                "name": "New User",
                "role": "Doctor",
                "blood_group": "B+",
                "date_of_birth": "1995-05-05",
                "gender": "Female",
                "phone_number": "+8801987654321",
                "password": "newpassword123",
                "password_confirm": "newpassword123",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/register.html")

    def test_log_in_view_valid(self):
        response = self.client.post(
            reverse("users-login"),
            {"username": "testuser@example.com", "password": "testpassword123"},
        )
        self.assertEqual(response.status_code, 302)  # Should redirect
        self.assertRedirects(response, reverse("home"))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_log_in_view_invalid(self):
        response = self.client.post(
            reverse("users-login"),
            {"username": "testuser@example.com", "password": "wrongpassword"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/login.htm")
        self.assertIn(
            "Invalid email or password",
            [m.message for m in messages.get_messages(response.wsgi_request)],
        )

    def test_log_out_view(self):
        self.client.login(username="testuser@example.com", password="testpassword123")
        response = self.client.get(reverse("users-logout"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home"))
        self.assertFalse(response.wsgi_request.user.is_authenticated)
