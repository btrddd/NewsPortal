import logging
from datetime import date, timedelta
 

from django.conf import settings
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


from news_feed.models import Post, Category
from NewsPortal.settings import DEFAULT_FROM_EMAIL
 
 
logger = logging.getLogger(__name__)
 
 
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

 
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)
 
 
class Command(BaseCommand):
    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")
        
        scheduler.add_job(
            weekly_category_subscription_emails,
            trigger=CronTrigger(second="*/10"),
            id="weekly_category_subscription_emails",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job: 'weekly_category_subscription_emails'.")
 
        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )
 
        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")