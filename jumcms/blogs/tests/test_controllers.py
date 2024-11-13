from django.test import TestCase
from django.urls import reverse
from blogs.models import Blog
from users.models import User
from django.utils import timezone

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
            title='Blog 1', 
            author=self.author_user,
            content='Content of blog 1',
            created_at=timezone.now()
        )
        self.blog2 = Blog.objects.create(
            title='Blog 2', 
            author=self.author_user,
            content='Content of blog 2',
            created_at=timezone.now()
        )
    
    def test_blog_list_view_status_code(self):
        """
        Test if the blog list view returns a 200 status code (OK)
        """
        url = reverse('blogs:blog-list')  # Ensure you use the correct URL name
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_blog_list_view_template(self):
        """
        Test if the correct template is used in the blog list view
        """
        url = reverse('blogs:blog-list')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'users/visit_seasonal_diseases.html')
    
    def test_blog_list_view_context_data(self):
        """
        Test if the correct blog posts are passed to the template
        """
        url = reverse('blogs:blog-list')
        response = self.client.get(url)
        blogs = response.context['blogs']
        self.assertEqual(len(blogs), 2)  # Check that 2 blog posts are passed to the context
        self.assertEqual(blogs[0].title, 'Blog 1')  # Ensure correct order
        self.assertEqual(blogs[1].title, 'Blog 2')
    
    def test_blog_detail_view_status_code(self):
        """
        Test if the blog detail view returns a 200 status code (OK) for valid blog
        """
        url = reverse('blogs:blog_detail', kwargs={'id': self.blog1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_blog_detail_view_template(self):
        """
        Test if the correct template is used in the blog detail view
        """
        url = reverse('blogs:blog_detail', kwargs={'id': self.blog1.id})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'users/blog_detail.html')
    
    def test_blog_detail_view_context_data(self):
        """
        Test if the correct blog is passed to the template
        """
        url = reverse('blogs:blog_detail', kwargs={'id': self.blog1.id})
        response = self.client.get(url)
        self.assertEqual(response.context['blog'].title, 'Blog 1')  # Check blog title
        self.assertEqual(response.context['blog'].content, 'Content of blog 1')  # Check content
    
    def test_blog_detail_view_invalid_blog(self):
        """
        Test that a redirect occurs when an invalid blog ID is provided (non-existing blog)
        """
        url = reverse('blogs:blog_detail', kwargs={'id': 9999})  # Use a non-existing blog ID
        response = self.client.get(url)
        # Assert that the response is a redirect (302)
        self.assertEqual(response.status_code, 302)
        # Assert that the redirect is to the blog list page
        self.assertRedirects(response, reverse('blogs:blog-list'))
