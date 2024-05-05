from apscheduler.schedulers.background import BackgroundScheduler
from jobs.jobs import send_mailings


def start():
    background = BackgroundScheduler()
    background.add_job(send_mailings, 'interval', seconds=15)
    background.start()
