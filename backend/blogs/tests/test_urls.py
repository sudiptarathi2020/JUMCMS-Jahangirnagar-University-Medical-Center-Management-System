# blogs/test_urls.py
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from blogs.controllers import create_blog_post, blog_list

class BlogURLsTests(SimpleTestCase):
    def test_create_blog_post_url_is_resolved(self):
        url = reverse('blogs:create-blog-post')  # Use the name defined in the urlpatterns
        self.assertEqual(resolve(url).func, create_blog_post)  # Check that the URL resolves to the correct view function

    def test_blog_list_url_is_resolved(self):
        url = reverse('blogs:blog-list')  # Use the name defined in the urlpatterns
        self.assertEqual(resolve(url).func, blog_list)  # Check that the URL resolves to the correct view function
