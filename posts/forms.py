from django import forms
from .models import Post
from pagedown.widgets import PagedownWidget


class PostForm(forms.ModelForm):
    publish = forms.DateField(widget=forms.SelectDateWidget)
    content = forms.CharField(widget=PagedownWidget)

    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'draft', 'publish']