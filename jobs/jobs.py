from config.settings import TIME_ZONE
import datetime
import pytz
from django.core.mail import send_mail
from emailing.models import Emailing, EmailingLog, Client
from config.settings import EMAIL_HOST_USER


def send_mailings():
    current_time = datetime.datetime.now(pytz.timezone(TIME_ZONE))
    for mailing in Emailing.objects.filter(emailing_status='создана'):
        recipients = [client.email for client in mailing.email.all()]

        if mailing.send_periodicity == 'daily' and current_time.hour == mailing.time_to_send.hour and current_time.minute == mailing.time_to_send.minute:
            message = mailing.message_set.all()
            send_mail(
                subject=message.topic,
                message=message.body,
                from_email=EMAIL_HOST_USER,
                recipient_list=recipients,
            )

        elif mailing.send_periodicity == 'weekly' and current_time.hour == mailing.time_to_send.hour and current_time.minute == mailing.time_to_send.minute and (current_time.day - mailing.time_to_send.day).days % 7 == 0:
            message = mailing.message_set.all()
            send_mail(
                subject=message.topic,
                message=message.body,
                from_email=EMAIL_HOST_USER,
                recipient_list=recipients,
            )

        elif mailing.send_periodicity == 'monthly' and current_time.hour == mailing.time_to_send.hour and current_time.minute == mailing.time_to_send.minute and (current_time.day - mailing.time_to_send.day).days % 30 == 0:
            message = mailing.message_set.all()
            send_mail(
                subject=message.topic,
                message=message.body,
                from_email=EMAIL_HOST_USER,
                recipient_list=recipients,
            )

        EmailingLog.objects.create(
            mailing=mailing,
            datatime_last_attempt=current_time,
            status_attempt='УСПЕШНО',
        )
