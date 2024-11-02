# blogs/test_views.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from blogs.forms import BlogForm
from blogs.models import Blog

User = get_user_model()

class BlogViewsTests(TestCase):
    def setUp(self):
        # Create a user to test the views
        self.superuser = User.objects.create_superuser(
            email='admin@example.com',
            name='Admin',
            password='asdf1234@',  # Choose a strong password
            role='admin',  # Or another appropriate role if 'admin' is not defined
            blood_group='A+',
            date_of_birth='1990-01-01',
            gender='Male',
            phone_number='+8801712345678',
        )
        self.client.login(username='admin@example.com', password='asdf1234@')  # Log in the user

    def test_create_blog_post_view_GET(self):
        response = self.client.get(reverse('blogs:create-blog-post'))  # URL for creating a blog post
        self.assertEqual(response.status_code, 200)  # Check for a successful response
        self.assertTemplateUsed(response, 'admin/create_blog.html')  # Ensure the correct template is used

    def test_create_blog_post_view_POST_valid(self):
        form_data = {
            'title': 'Test Blog Title',
            'content': 'This is a test blog content.',
            'image': 'static.images.default_user.png',
            'tags': "test"
        }
        response = self.client.post(reverse('blogs:create-blog-post'), data=form_data)  # Submit the form
        self.assertRedirects(response, reverse('blogs:blog-list'))  # Check for redirect after successful creation
        self.assertEqual(Blog.objects.count(), 1)  # Ensure a blog post was created
        self.assertEqual(Blog.objects.first().title, 'Test Blog Title')  # Check the title of the created blog post

    def test_create_blog_post_view_POST_invalid(self):
        form_data = {
            'title': '',  # Empty title should be invalid
            'content': 'This is a test blog content.',
            'image': 'static.images.default_user.png',
            'tags': 'test, blog, django'
        }
        form = BlogForm(data=form_data)
        response = self.client.post(reverse('blogs:create-blog-post'), form_data=form_data)  # Submit the form
        self.assertEqual(response.status_code, 200)  # Should render the form again
        self.assertTrue(form.errors)

    def test_blog_list_view(self):
        # Create a blog post to test the blog list view
        Blog.objects.create(title='Test Blog Title', content='This is a test blog content.', author=self.superuser)
        response = self.client.get(reverse('blogs:blog-list'))  # URL for the blog list
        self.assertEqual(response.status_code, 200)  # Check for a successful response
        self.assertTemplateUsed(response, 'admin/blog_list.html')  # Ensure the correct template is used
        self.assertContains(response, 'Test Blog Title')  # Check if the blog title is in the response
