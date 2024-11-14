from django.test import TestCase
from django.urls import reverse
from blogs.models import Blog
from users.models import User
from django.utils import timezone
from datetime import timedelta
from blogs.forms import BlogForm


class BlogListViewTests(TestCase):

    def setUp(self):
        # Create a user (author) for the blogs
        self.author_user = User.objects.create_user(
            email="testuser@example.com",
            name="Test User",
            role="Patient",
            blood_group="A+",
            date_of_birth="2000-01-01",
            gender="Male",
            phone_number="+8801234567890",
            password="testpassword123",
        )
        self.author_user.is_approved = True
        self.author_user.save()  # Save user to commit it to the database

        # Create blog posts associated with the author
        self.blog1 = Blog.objects.create(
            title="Blog 1",
            author=self.author_user,
            content="Content of blog 1",
            created_at=timezone.now() - timedelta(minutes=5),
        )
        self.blog2 = Blog.objects.create(
            title="Blog 2",
            author=self.author_user,
            content="Content of blog 2",
            created_at=timezone.now(),
        )

    def test_blog_list_view_status_code(self):
        """
        Test if the blog list view returns a 200 status code (OK)
        """
        url = reverse("blogs:blog-list")  # Ensure you use the correct URL name
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_blog_list_view_template(self):
        """
        Test if the correct template is used in the blog list view
        """
        url = reverse("blogs:blog-list")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "users/visit_seasonal_diseases.html")

    def test_blog_list_view_context_data(self):
        """
        Test if the correct blog posts are passed to the template
        """
        url = reverse("blogs:blog-list")
        response = self.client.get(url)
        blogs = response.context["blogs"]
        self.assertEqual(
            len(blogs), 2
        )  # Check that 2 blog posts are passed to the context
        self.assertEqual(blogs[0].title, "Blog 2")  # Ensure correct order
        self.assertEqual(blogs[1].title, "Blog 1")

    def test_blog_detail_view_status_code(self):
        """
        Test if the blog detail view returns a 200 status code (OK) for valid blog
        """
        url = reverse("blogs:blog_detail", kwargs={"id": self.blog1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_blog_detail_view_template(self):
        """
        Test if the correct template is used in the blog detail view
        """
        url = reverse("blogs:blog_detail", kwargs={"id": self.blog1.id})
        response = self.client.get(url)
        self.assertTemplateUsed(response, "users/blog_detail.html")

    def test_blog_detail_view_context_data(self):
        """
        Test if the correct blog is passed to the template
        """
        url = reverse("blogs:blog_detail", kwargs={"id": self.blog1.id})
        response = self.client.get(url)
        self.assertEqual(response.context["blog"].title, "Blog 1")  # Check blog title
        self.assertEqual(
            response.context["blog"].content, "Content of blog 1"
        )  # Check content

    def test_blog_detail_view_invalid_blog(self):
        """
        Test that a redirect occurs when an invalid blog ID is provided (non-existing blog)
        """
        url = reverse(
            "blogs:blog_detail", kwargs={"id": 9999}
        )  # Use a non-existing blog ID
        response = self.client.get(url)
        # Assert that the response is a redirect (302)
        self.assertEqual(response.status_code, 302)
        # Assert that the redirect is to the blog list page
        self.assertRedirects(response, reverse("blogs:blog-list"))


class BlogControllersTests(TestCase):
    def setUp(self):
        # Create a user to test the views
        self.superuser = User.objects.create_superuser(
            email="admin@example.com",
            name="Admin",
            password="asdf1234@",  # Choose a strong password
            role="admin",  # Or another appropriate role if 'admin' is not defined
            blood_group="A+",
            date_of_birth="1990-01-01",
            gender="Male",
            phone_number="+8801712345678",
        )
        self.client.login(
            username="admin@example.com", password="asdf1234@"
        )  # Log in the user

    def test_create_blog_post_view_GET(self):
        response = self.client.get(
            reverse("blogs:create-blog-post")
        )  # URL for creating a blog post
        self.assertEqual(response.status_code, 200)  # Check for a successful response
        self.assertTemplateUsed(
            response, "admin/create_blog.html"
        )  # Ensure the correct template is used

    def test_create_blog_post_view_POST_valid(self):
        form_data = {
            "title": "Test Blog Title",
            "content": "This is a test blog content.",
            "image": "static.images.default_user.png",
            "tags": "test",
        }
        response = self.client.post(
            reverse("blogs:create-blog-post"), data=form_data
        )  # Submit the form
        self.assertRedirects(
            response, reverse("blogs:blog-list")
        )  # Check for redirect after successful creation
        self.assertEqual(Blog.objects.count(), 1)  # Ensure a blog post was created
        self.assertEqual(
            Blog.objects.first().title, "Test Blog Title"
        )  # Check the title of the created blog post

    def test_create_blog_post_view_POST_invalid(self):
        form_data = {
            "title": "",  # Empty title should be invalid
            "content": "This is a test blog content.",
            "image": "static.images.default_user.png",
            "tags": "test, blog, django",
        }
        form = BlogForm(data=form_data)
        response = self.client.post(
            reverse("blogs:create-blog-post"), form_data=form_data
        )  # Submit the form
        self.assertEqual(response.status_code, 200)  # Should render the form again
        self.assertTrue(form.errors)

    def test_blog_list_view(self):
        # Create a blog post to test the blog list view
        Blog.objects.create(
            title="Test Blog Title",
            content="This is a test blog content.",
            author=self.superuser,
        )
        response = self.client.get(
            reverse("blogs:blog-list-for-admin")
        )  # URL for the blog list
        self.assertEqual(response.status_code, 200)  # Check for a successful response
        self.assertTemplateUsed(
            response, "admin/blog_list.html"
        )  # Ensure the correct template is used
        self.assertContains(
            response, "Test Blog Title"
        )  # Check if the blog title is in the response
