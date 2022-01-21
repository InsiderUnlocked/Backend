from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import register_events, DjangoJobStore
from congress.views import updateDB


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), 'djangojobstore')
    # Updates database every 24 hours
    scheduler.add_job(updateDB, 'interval', days=1)

    register_events(scheduler)

    # @scheduler.scheduled_job('cron', hour=1, name='updateData')
    # @scheduler.scheduled_job('interval', seconds=1, name='updateData')
    # def updateData():
    #     updateDB()

    scheduler.start()
