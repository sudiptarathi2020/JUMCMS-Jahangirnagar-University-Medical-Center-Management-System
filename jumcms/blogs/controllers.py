
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from blogs.forms import BlogForm
from blogs.models import Blog

# blogPart Start (Hasan)
@login_required
def create_blog_post(request):
    """
    Handles the creation of a new blog post.

    This view requires the user to be logged in. If the request method is POST,
    it processes the submitted form. If the form is valid, it saves the blog post
    with the current user as the author and redirects to the blog list.

    Args:
        request (HttpRequest): The request object containing metadata about the request.

    Returns:
        HttpResponse: A redirect to the blog list or renders the blog creation form.
    """
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            Blog = form.save(commit=False)
            Blog.author = request.user
            Blog.save()
            return redirect('blogs/blog_list')  # Redirect to a blog list or success page
    else:
        form = BlogForm()
    return render(request, 'blogs/create_blog.html', {'form': form})


def blog_list(request):
    """
    Displays a list of all blog posts.

    This view retrieves all blog posts from the database, ordered by their creation
    date in descending order, and renders them in a template.

    Args:
        request (HttpRequest): The request object containing metadata about the request.

    Returns:
        HttpResponse: A rendered template displaying the list of blogs.
    """
    blogs = Blog.objects.all().order_by('-created_at')  # Retrieve all blogs ordered by creation date
    return render(request, 'blogs/blog_list.html', {'blogs': blogs})
# Blog Part (Hasan)