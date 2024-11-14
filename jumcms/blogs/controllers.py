from django.shortcuts import render, redirect
from blogs.models import Blog

# Create your views here.


def blog_list(request):
    """
    Displays seasonal diseases portal

    This view retrieves all blog posts from the database, ordered by their creation
    date in descending order, and renders them in a template.This blog post mainly shows the
    seasonal disesases thats occur during different seasons.

    Args:
        request (HttpRequest): The request object containing metadata about the request.

    Returns:
        HttpResponse: A rendered template displaying the list of blogs.
    """
    blogs = Blog.objects.all().order_by('-created_at')  # Retrieve all blogs ordered by creation date
    return render(request, 'users/visit_seasonal_diseases.html', {'blogs': blogs})

def blog_detail(request, id):
    try:
        blog = Blog.objects.get(id=id)
    except Blog.DoesNotExist:
        # If blog does not exist, redirect to blog list page
        return redirect('blogs:blog-list')

    return render(request, 'users/blog_detail.html', {'blog': blog})
