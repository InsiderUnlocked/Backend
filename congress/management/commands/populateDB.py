# @Author: Mohammed-Al Rasheed
# Purpose: Create a custom command to populate the database using: "python manage.py populateDB"

# Imports
from django.core.management.base import BaseCommand
from django.core.management import call_command
import logging

# Import scripts and models to populate the database
from ...models import CongressPerson, CongressTrade, Ticker, SummaryStat
from ...populate import historical as historicalPopulate
from ...populate import current as currentPopulate

# Create custom command
class Command(BaseCommand):
    # Help message: "python manage.py populateDB --help"
    help = 'Run this command to initially populate the database. Type "python manage.py populateDB" to run'

    def handle(self, *args, **options):
        # Log that we are now starting to populate the database
        logging.info("Populating database...")
        
        # Call the populate scripts

        # Add Ticker Table (load it in from json file as it takes a lot of time to load it)
        call_command('loaddata', 'ticker.json')
        logging.info("Finished populating tickers table")

        # Load the transactions into the database from the transactions.json file and add it to the database
        historicalPopulate()
        logging.info("Finished populating historical congress trades")
 
        # Add the most recent transactions into the database
        currentPopulate()
        logging.info("Finished populating recent congress trades")        

        # Create the Summary Stats and update them to populate them with recent data
        # We only want to show summarized data from the following timeframes

        # check if there are no created summary stats objects
        if SummaryStat.objects.count() == 0:
            timeframes = [30, 60, 90, 120] 
            
            # Loop through the timeframes and update the summary stats
            for timeframe in timeframes:
                # Create a SummaryStat object for each timeframe
                obj = SummaryStat.objects.create(timeframe=timeframe)
                # Update the summary stats for each timeframe using updatedStats()
                obj.updateStats()
            
        logging.info("Finished populating summary stats")

        # Log that we have finished populating the database
        logging.info("Database Updated")