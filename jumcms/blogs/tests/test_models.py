from django.test import TestCase
from blogs.models import Blog
from django.contrib.auth import get_user_model

User = get_user_model()

class BlogModelTests(TestCase):
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
            role_id = "aaaaaa",
        )
        self.client.login(username='admin@example.com', password='asdf1234@')  # Log in the user

    def test_blog_creation(self):
        # Create a new blog post
        blog = Blog.objects.create(
            title='Test Blog',
            author=self.superuser,
            content='This is a test blog post.',
            tags='test, blog'
        )

        # Verify that the blog post is created and fields are populated correctly
        self.assertEqual(blog.title, 'Test Blog')
        self.assertEqual(blog.author, self.superuser)
        self.assertEqual(blog.content, 'This is a test blog post.')
        self.assertEqual(blog.tags, 'test, blog')
        self.assertIsNotNone(blog.created_at)  # Check that created_at is set
        self.assertIsNotNone(blog.updated_at)  # Check that updated_at is set

    def test_blog_str_method(self):
        # Create a new blog post
        blog = Blog.objects.create(
            title='Test Blog for String Method',
            author=self.superuser,
            content='This blog is for testing the __str__ method.'
        )

        # Check that the string representation of the blog is correct
        self.assertEqual(str(blog), 'Test Blog for String Method')

