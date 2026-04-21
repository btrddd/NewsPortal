from django.contrib import admin
from .models import Post, Author, Category


def delete_category_posts(modeladmin, request, queryset):
    for obj in queryset:
        Post.objects.filter(category=obj).delete()
delete_category_posts.short_description = 'Удалить все публикации в категории'


def delete_author_posts(modeladmin, request, queryset):
    for obj in queryset:
        Post.objects.filter(author=obj).delete()
delete_author_posts.short_description = 'Удалить все публикации автора'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        'date_time',
        'post_type',
        'author__user__username', 
        'title', 
        'text', 
        'rating',
    ]

    list_filter = ['category__category_name', 'rating', 'date_time', 'post_type']
    search_fields = ['author__user__username', 'title', 'text']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name', 'post_count']
    search_fields = ['category_name']
    actions = [delete_category_posts]


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['user__username', 'rating', 'post_count']
    list_filter = ['rating']
    search_fields = ['user__username']
    actions = [delete_author_posts]
