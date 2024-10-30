from django import forms
from blogs.models import Blog

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'image', 'tags']
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter blog title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter blog content'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add tags, separated by commas'}),
        }
