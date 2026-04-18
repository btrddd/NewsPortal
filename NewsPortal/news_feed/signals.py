from django.template.loader import render_to_string
from django.db.models.signals import m2m_changed, pre_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.core.exceptions import ValidationError
from datetime import date


from NewsPortal.settings import DEFAULT_FROM_EMAIL
from .models import Post, Category
from .tasks import post_email_message


@receiver(signal=m2m_changed, sender=Post.category.through)
def new_post_email_message(sender, instance: Post, action, **kwargs):
    if action != 'post_add':
        return
    
    subscribers = set()
    for category in instance.category.all():
        category: Category
        subscribers.update(
            set(category.subscribers.values_list('username', 'email'))
        )
    
    post_email_message.apply_async([list(subscribers), instance.pk, category.category_name])
    

@receiver(signal=pre_save, sender=Post)
def post_limit_reached_check(sender, instance: Post, **kwargs):
    if instance.pk:
        return
    
    todays_user_posts = Post.objects.filter(
        author=instance.author, 
        date_time__icontains=date.today()
    )
    
    if len(todays_user_posts) >= Post.POST_LIMIT:
        raise ValidationError(
            f'Превышен лимит ({Post.POST_LIMIT}) публикаций за сегодня.'
        )
