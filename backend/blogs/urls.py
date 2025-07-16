from django.urls import path
from blogs.controllers import (
    create_blog_post,
    blog_list,
    blog_detail,
    blog_list_for_admin,
)

app_name = "blogs"
urlpatterns = [
    path("create_blog/", create_blog_post, name="create-blog-post"),
    path("see_blogs/", blog_list_for_admin, name="blog-list-for-admin"),
    path("", blog_list, name="blog-list"),
    path("blog/<int:id>/", blog_detail, name="blog_detail"),
]
