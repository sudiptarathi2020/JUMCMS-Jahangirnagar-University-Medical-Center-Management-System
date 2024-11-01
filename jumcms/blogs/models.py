from django.db import models
from users.models import User


# Create your models here.
class Blog(models.Model):
    """
    Represents a blog post.

    Attributes:
        title (CharField): The title of the blog post, with a maximum length of 255 characters.
        author (ForeignKey): A reference to the User who authored the blog post. 
                             The relationship is a one-to-many, where a user can have multiple blog posts.
        content (TextField): The content of the blog post.
        created_at (DateTimeField): The date and time when the blog post was created, set automatically.
        updated_at (DateTimeField): The date and time when the blog post was last updated, set automatically.
        image (ImageField): An optional image associated with the blog post, stored in the 'blog_images/' directory.
        tags (CharField): A field for adding tags to the blog post, separated by commas, with a maximum length of 255 characters.

    Methods:
        __str__(): Returns the title of the blog post when the object is printed.
    """
    title = models.CharField(max_length=255)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="blog_images/", null=True, blank=True)
    tags = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title
