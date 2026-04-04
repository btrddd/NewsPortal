from django import forms
from django.core.exceptions import ValidationError


from .models import Post, Author, Category


class PostForm(forms.ModelForm):
    author = forms.ModelChoiceField(
        label='Автор', 
        empty_label=None, 
        queryset=Author.objects,
    )
    
    category = forms.ModelMultipleChoiceField(
        label='Категории',
        queryset=Category.objects
    )

    title = forms.CharField(
        label='Заголовок',
        max_length=255,
        min_length=10
    )

    text = forms.CharField(
        label='Текст публикации',
        widget=forms.Textarea,
        min_length=255
    )


    class Meta:
        model = Post
        fields = ['author', 'category', 'title', 'text']
