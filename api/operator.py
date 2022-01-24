# @Author: Farhan Rehman
# Purpose: update database every 24 hours by fetching data from the official website (efdsearch.senate.gov) and inserting it into our databse

# Imports
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import register_events, DjangoJobStore

# Updates database every 24 hours
def updateDB(): 
    logging.info("started update")

    # update the database with the latest data from the official website
    currentPopulate()
    # log that the database update has been updated
    logging.info("Finished populating recent congress trades")

    # Get all summaryStats objects
    summaryStats = SummaryStat.objects.all()

    # For each summaryStat, update the stats with the latest data
    for summaryStat in summaryStats:
        summaryStat.updateStats()

    # log that the database has been fully updated
    logging.info("Database Updated")

# Function creates a scheduler and registers the updateDB function to run every 24 hours
def start():
    # Initilaize background scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), 'djangojobstore')
    
    # Set schedule touUpdates database every 24 hours
    scheduler.add_job(updateDB, 'interval', days=1)

    # register schculed events
    register_events(scheduler)

    # Start scheduler
    scheduler.start()
