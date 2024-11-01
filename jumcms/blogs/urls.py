

from django.urls import path
from blogs.controllers import create_blog_post, blog_list

urlpatterns = [
    path("create_blog/", create_blog_post, name="create-blog-post"),
    path("see_blogs/", blog_list, name="blog-list"),
]
