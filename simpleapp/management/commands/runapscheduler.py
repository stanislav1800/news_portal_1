import datetime
import logging
from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.core.mail import EmailMultiAlternatives
from simpleapp.models import Post, Category

logger = logging.getLogger(__name__)

def my_job():
    categories = Category.objects.all()
    for category in categories:
        subscribers = category.subscribers.all()
        posts = Post.objects.filter(category=category, date__gte=datetime.datetime.now() - datetime.timedelta(days=7))
        if posts.exists():
            subject = f'Новые статьи в категории {category}'
            html_context = render_to_string(
                'weekly_notifications_email.html',
                {
                    'categ': category,
                    'posts': posts,
                    'link': f'{settings.SITE_URL}/news/'
                }
            )
            msg = EmailMultiAlternatives(
                subject=subject,
                body='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[s.email for s in subscribers],
            )
            msg.attach_alternative(html_context, 'text/html')
            msg.send()


def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            #trigger=CronTrigger(day_of_week='mon', hour='12', minute='30'),
            trigger=CronTrigger(second="*/10"),
            id = "my_job",
            max_instances = 1,
            replace_existing = True,
        )
        logger.info("Added job 'my_job'.")

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