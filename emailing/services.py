import logging
import smtplib
import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.mail import send_mail
from django.core.management import BaseCommand
from datetime import datetime
from django_apscheduler.jobstores import DjangoJobStore, logger

from emailing.models import EmailingLog, Emailing


logger = logging.getLogger(__name__)


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_email, 'interval', seconds=30)
    scheduler.start()


def send_email():
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)
    emailing = Emailing.objects.all()

    for e in emailing:
        if e.start_time <= current_datetime < e.end_time and e.emailing_status != Emailing.STATUS_DONE and e.is_active:
            clients = e.emailing_clients.all()
            clients_emails = [clients.email for clients in clients]
            message_topic = e.message.topic
            message_body = e.message.body

            e.status = Emailing.STATUS_STARTED

            try:
                send_mail(
                    subject=message_topic,
                    message=message_body,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=clients_emails,
                    fail_silently=False,
                )
                response = "Рассылка успешно отправлена"

            except smtplib.SMTPException as ex:
                response = f"Ошибка при отправке письма: {str(ex)}"
            finally:
                new = EmailingLog.objects.create(
                    last_try=current_datetime,
                    response=response,
                )
                new.client.add(*clients)
                new.save()

            if e.send_periodicity == Emailing.PERIOD_DAILY:
                e.start_time += datetime.timedelta(days=1, hours=0, minutes=0)
            elif e.send_periodicity == Emailing.PERIOD_WEEKLY:
                e.start_time += datetime.timedelta(days=7, hours=0, minutes=0)
            elif e.send_periodicity == Emailing.PERIOD_MONTHLY:
                e.start_time += datetime.timedelta(days=30, hours=0, minutes=0)
        elif current_datetime >= e.end_time and e.start_time > e.end_time:
            e.emailing_status = Emailing.STATUS_DONE
        elif current_datetime < e.start_time:
            e.emailing_status = Emailing.STATUS_CREATED

        e.save()


class Command(BaseCommand):
    help = "Runs APScheduler"

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            send_email(),
            trigger=CronTrigger(month=30),
            id="sendmail",
            max_instances=1,
            replace_existing=True
        )
        logger.info("Added job 'sendmail'")
        try:
            logger.info("Started scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopped scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
