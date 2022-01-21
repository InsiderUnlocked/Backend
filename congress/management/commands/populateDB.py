from ...models import CongressPerson, CongressTrade, Ticker, SummaryStat
from django.core.management.base import BaseCommand
import logging

# Import scripts to populate the database
from ...scripts.congressPeople import main as updateCongressPersonMain
from ...populate import historical as historicalPopulate
from ...populate import current as currentPopulate
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Run this command to initially populate the database'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        logging.info("Populating database...")
        # Add/Update CongressPerson Table (Get all members)
        try: 
            updateCongressPersonMain()
            logging.info("Finished populating congress people table")
        except: 
            logging.error("ERROR: updating CongressPerson table")

        try:
            call_command('loaddata', 'ticker.json')
            logging.info("Finished populating tickers table")
        except Exception as e:
            logging.error("ERROR: updating Tickers table")
            logging.error(e)

        try: 
            historicalPopulate()
            logging.info("Finished populating historical congress trades")
        except: 
            logging.error("ERROR: updating Historical CongressTrades table")

        try: 
            currentPopulate()
            logging.info("Finished populating recent congress trades")
        except: 
            logging.error("ERROR: updating Current CongressTrades table")
        
        # Create Summary  Stats
        try:
            for timeframe in range(30, 150, 30):
                obj = SummaryStat.objects.create(timeframe=timeframe)
                obj.updateStats()
            
            logging.info("Finished populating summary stats")

        except Exception as e:
            print(e)
            logging.error("ERROR: creating Summary Stats table")

        logging.info("Database Updated")