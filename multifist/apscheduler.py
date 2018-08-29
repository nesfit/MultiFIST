from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore

APScheduler = BackgroundScheduler()
APScheduler.add_jobstore(DjangoJobStore(), "default")
APScheduler.start()
print("Scheduler started !!!")