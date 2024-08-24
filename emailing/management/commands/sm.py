from django.core.management.base import BaseCommand
from django_apscheduler import util
from django_apscheduler.models import DjangoJobExecution
from emailing.services import send_email


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler"

    def handle(self, *args, **options):
        send_email()
