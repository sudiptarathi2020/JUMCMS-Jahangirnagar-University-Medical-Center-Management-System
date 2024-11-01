# blogs/test_views.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from blogs.models import Blog

User = get_user_model()

class BlogViewsTests(TestCase):
    def setUp(self):
        # Create a user to test the views
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')  # Log in the user

    def test_create_blog_post_view_GET(self):
        response = self.client.get(reverse('create-blog-post'))  # URL for creating a blog post
        self.assertEqual(response.status_code, 200)  # Check for a successful response
        self.assertTemplateUsed(response, 'blogs/create_blog.html')  # Ensure the correct template is used

    def test_create_blog_post_view_POST_valid(self):
        form_data = {
            'title': 'Test Blog Title',
            'content': 'This is a test blog content.',
            'image': None,  # No image for this test
            'tags': 'test, blog, django'
        }
        response = self.client.post(reverse('create-blog-post'), data=form_data)  # Submit the form
        self.assertRedirects(response, reverse('blog-list'))  # Check for redirect after successful creation
        self.assertEqual(Blog.objects.count(), 1)  # Ensure a blog post was created
        self.assertEqual(Blog.objects.first().title, 'Test Blog Title')  # Check the title of the created blog post

    def test_create_blog_post_view_POST_invalid(self):
        form_data = {
            'title': '',  # Empty title should be invalid
            'content': 'This is a test blog content.',
            'image': None,
            'tags': 'test, blog, django'
        }
        response = self.client.post(reverse('create-blog-post'), data=form_data)  # Submit the form
        self.assertEqual(response.status_code, 200)  # Should render the form again
        self.assertFormError(response, 'form', 'title')  # Check for a form error on the title field

    def test_blog_list_view(self):
        # Create a blog post to test the blog list view
        Blog.objects.create(title='Test Blog Title', content='This is a test blog content.', author=self.user)
        response = self.client.get(reverse('blog-list'))  # URL for the blog list
        self.assertEqual(response.status_code, 200)  # Check for a successful response
        self.assertTemplateUsed(response, 'blogs/blog_list.html')  # Ensure the correct template is used
        self.assertContains(response, 'Test Blog Title')  # Check if the blog title is in the response
