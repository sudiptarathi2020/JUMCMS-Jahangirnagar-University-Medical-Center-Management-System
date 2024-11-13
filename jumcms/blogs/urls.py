
from django.urls import path
from blogs.controllers import blog_list, blog_detail

app_name = 'blogs'
urlpatterns = [
    path("", blog_list, name="blog-list"),
    path('blog/<int:id>/',blog_detail, name='blog_detail'),
]
