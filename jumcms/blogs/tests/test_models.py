from django.test import TestCase
from users.models import Blog
from django.contrib.auth import get_user_model

User = get_user_model()

class BlogModelTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_blog_creation(self):
        # Create a new blog post
        blog = Blog.objects.create(
            title='Test Blog',
            author=self.user,
            content='This is a test blog post.',
            tags='test, blog'
        )
        
        # Verify that the blog post is created and fields are populated correctly
        self.assertEqual(blog.title, 'Test Blog')
        self.assertEqual(blog.author, self.user)
        self.assertEqual(blog.content, 'This is a test blog post.')
        self.assertEqual(blog.tags, 'test, blog')
        self.assertIsNotNone(blog.created_at)  # Check that created_at is set
        self.assertIsNotNone(blog.updated_at)  # Check that updated_at is set

    def test_blog_str_method(self):
        # Create a new blog post
        blog = Blog.objects.create(
            title='Test Blog for String Method',
            author=self.user,
            content='This blog is for testing the __str__ method.'
        )
        
        # Check that the string representation of the blog is correct
        self.assertEqual(str(blog), 'Test Blog for String Method')

