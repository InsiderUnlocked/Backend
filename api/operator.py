# @Author: Farhan Rehman
# Purpose: update database every 24 hours by fetching data from a webside and inserting it into our databse

# Imports
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import register_events, DjangoJobStore

# Updates database every 24 hours
def updateDB(): 
    # Look at at each table, if any table is empty, populate it with historical data
    logging.info("started update")

    # If none of the tables are empty update it with current data
    try: 
        currentPopulate()
        logging.info("Finished populating recent congress trades")

    except: 
        logging.error("ERROR: updating CongressPerson table")

    try:
        # Get all summaryStats
        summaryStats = SummaryStat.objects.all()

        # For each summaryStat, update the stats
        for summaryStat in summaryStats:
            summaryStat.updateStats()

    except:
        logging.error("ERROR: updating Summary Stats table")
    
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
