from django import forms
from blogs.models import Blog

# Blog Part Start(Hasan)
class BlogForm(forms.ModelForm):
    """
    A form for creating and updating blog posts.

    This form is based on the Blog model and includes fields for the blog title,
    content, image, and tags. It customizes the widgets for a better user experience.

    Attributes:
        title (CharField): The title of the blog post.
        content (TextField): The content of the blog post.
        image (ImageField): An optional image associated with the blog post.
        tags (CharField): A field for adding tags to the blog post, separated by commas.

    Meta:
        model (Blog): The model associated with this form.
        fields (list): A list of fields included in the form.
        widgets (dict): Custom widgets for styling form fields.
    """
    class Meta:
        model = Blog
        fields = ['title', 'content', 'image', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter blog title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter blog content'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add tags, separated by commas'}),
        }
# Blog Part End (Hasan)