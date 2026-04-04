from django_filters import FilterSet, CharFilter, DateFilter
from django import forms
from .models import Post


class PostFilter(FilterSet):
    model = Post

    author = CharFilter(
        field_name='author__user__username',
        lookup_expr='icontains',
        label='Автор'
    )

    title = CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Заголовок содержит'
    )

    date_time = DateFilter(
        field_name='date_time',
        lookup_expr='gte',
        label='Дата публикации позже',
        widget = forms.DateInput(attrs={
            'type': 'date',
            'placeholder': 'DD/MM/YYYY'
            }
        )
    )
