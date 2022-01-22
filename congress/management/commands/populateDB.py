# @Author: Farhan Rehman
# Purpose: Create a custom command to populate the database using: "python manage.py populateDB"

# Imports
from django.core.management.base import BaseCommand
import logging

# Import scripts and models to populate the database
from ...models import CongressPerson, CongressTrade, Ticker, SummaryStat
from ...scripts.congressPeople import main as updateCongressPersonMain
from ...populate import historical as historicalPopulate
from ...populate import current as currentPopulate
from django.core.management import call_command

# Create custom command
class Command(BaseCommand):
    # Help message: "python manage.py populateDB --help"
    help = 'Run this command to initially populate the database. Type "python manage.py populateDB" to run'

    def handle(self, *args, **options):
        logging.info("Populating database...")
        
        # Call the populate scripts
        
        # Add/Update CongressPerson Table (Get all members)
        try: 
            updateCongressPersonMain()
            logging.info("Finished populating congress people table")
        except: 
            logging.error("Updating CongressPerson table")

        # Add Ticker Table (load it in from json file as it takes a lot of time to load it)
        try:
            call_command('loaddata', 'ticker.json')
            logging.info("Finished populating tickers table")
        except Exception as e:
            logging.error("Updating Tickers table")
            logging.error(e)

        # Load the transactions into the database from the transactions.json file and add it to the database
        try: 
            historicalPopulate()
            logging.info("Finished populating historical congress trades")
        except: 
            logging.error("Updating Historical CongressTrades table")

        # Add the most recent transactions into the database
        try: 
            currentPopulate()
            logging.info("Finished populating recent congress trades")
        except: 
            logging.error("Updating Current CongressTrades table")
        

        # Create the Summary Stats and update them to populate them with recent data
        try:
            # We only want to show summarized data from the following timeframes
            timeframes = [30, 60, 90, 120] 
            # Loop through the timeframes and update the summary stats
            for timeframe in timeframes:
                obj = SummaryStat.objects.create(timeframe=timeframe)
                obj.updateStats()
            
            logging.info("Finished populating summary stats")

        except Exception as e:
            print(e)
            logging.error("ERROR: creating Summary Stats table")

        logging.info("Database Updated")