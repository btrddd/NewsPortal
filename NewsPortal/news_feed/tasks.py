from datetime import date, timedelta
from celery import shared_task
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


from .models import Post, Category
from NewsPortal.settings import DEFAULT_FROM_EMAIL


@shared_task
def post_email_message(subscribers, post_id, category_name):
    post = Post.objects.get(pk=post_id)

    for subscriber in subscribers:
        html_content = render_to_string(
            'post/post_email_message.html',
            {
                'post': post,
                'username': subscriber[0],
                'category': category_name,
            }
        )

        message = EmailMultiAlternatives(
            subject=post.title,
            body=post.text,
            from_email=DEFAULT_FROM_EMAIL,
            to=[subscriber[1]]
        )

        message.attach_alternative(html_content, 'text/html')
        message.send()
    

@shared_task
def weekly_category_subscription_emails():
    for category in Category.objects.all():
        week_ago = date.today() - timedelta(days=7)
        posts = Post.objects.filter(category=category, date_time__gte=week_ago)

        if not posts:
            return
        
        for subscriber in category.subscribers.values_list('username', 'email'):
            html_content = render_to_string(
                'post/post_weekly_email_message.html',
                {
                    'posts': posts,
                    'category': category.category_name,
                    'username': subscriber[0],
                }
            )

            message = EmailMultiAlternatives(
                subject=f'Публикации вашей любимой категории "{category.category_name}", которые вы могли пропустить!',
                from_email=DEFAULT_FROM_EMAIL,
                to=[subscriber[1]]
            )

            message.attach_alternative(html_content, 'text/html')
            message.send()
