from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.cache import cache


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        posts_rating = Post.objects.filter(author=self).aggregate(models.Sum('rating'))['rating__sum']*3
        comments_rating = Comment.objects.filter(user=self.user).aggregate(models.Sum('rating'))['rating__sum']
        posts_comments_rating = Comment.objects.filter(
            post__in=[*Post.objects.filter(author=self)]).aggregate(models.Sum('rating'))['rating__sum']

        self.rating = posts_rating + comments_rating + posts_comments_rating
        self.save()

    def __str__(self):
        return f'{self.user}'
    
    @property
    def post_count(self):
        return len(Post.objects.filter(author=self))


class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, through='CategorySubscribers')

    def __str__(self):
        return f'{self.category_name}'
    
    @property
    def post_count(self):
        return len(Post.objects.filter(category=self))


class Post(models.Model):
    POST_LIMIT = 3
    article = 'AR'
    news = 'NE'

    POST_TYPES = [
        (article, 'Статья'), 
        (news, 'Новость'),
    ]

    author = models.ForeignKey(Author, on_delete=models.SET('Неизвестный автор'))
    post_type = models.CharField(max_length=2, choices=POST_TYPES, default='NE')
    date_time = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def prewiew(self):
        return self.text[:123] + '...'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'{self.title}: {self.prewiew()}'
    
    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'post-{self.pk}')


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=1000)
    date_time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class CategorySubscribers(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('category', 'user')
        