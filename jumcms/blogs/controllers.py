
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from blogs.forms import BlogForm
from blogs.models import Blog


@login_required
def create_blog_post(request):
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
    blogs = Blog.objects.all().order_by('-created_at')  # Retrieve all blogs ordered by creation date
    return render(request, 'blogs/blog_list.html', {'blogs': blogs})
