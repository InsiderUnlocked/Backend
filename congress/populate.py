# @Author: Farhan Rehman
# Purpose: The purpose of this script is to populate the database with historical data, and then update the database with the current data.

# Imports
from django.db.models import Q

from .models import CongressPerson, Ticker, CongressTrade
from .scripts.senators import main as getSenatorData
from .scripts.ticker import getTickerData

import datetime
import logging
import json
import time

# Get or Create Ticker Object
# Parameter: ticker (string)
def getTicker(stockTicker):
    try:
        # If the ticker is equal to "--", or "-" then return None as it is not a stock ticker 
        if stockTicker == "--" or stockTicker == "-":
            return None

        # Check to see if the stock ticker is already in the database, if not, create it
        # tickerObj holds the object
        # created is a boolean value which indicates if the object has been created or not
        tickerObj, created = Ticker.objects.get_or_create(ticker=stockTicker)

        # If the stock ticker has just beed created and also dont look for information for stock tickers that have periods or dashes in them
        if created == True and '.' not in stockTicker and '-' not in stockTicker:
            # Get more data about the stock ticker
            sector, industry, company, marketcap, quoteType = getTickerData(stockTicker)
            
            # if the quoteType is not an ETF
            if quoteType != "ETF":
                # Assign the stock ticker information to the newly created ticker objects fields
                tickerObj.sector = sector

                tickerObj.industry = industry

                tickerObj.company = company

                tickerObj.marketcap = marketcap
            else:
                # If the ticker is an ETF, then set the sector to ETF which would be quoteType
                tickerObj.sector = quoteType

            # Save the changes to the database
            tickerObj.save()

        # Return the ticker object
        return tickerObj

    except Exception as e:
        # Error checking for possible errors as we gradually scale our database
        logging.error("Error while creating a stock ticker object")
        logging.error(e)


# Get or Create Congress Person Object
# Parameter: name (string)
def getCongressPerson(name):
    try:
        # find congress person object in database table CongressPerson
    
        # remove trailing whitespace
        name = name.strip()
        # replace commas
        name = name.replace(",", "")
        # remove periods
        name = name.replace(".", "")

        # Check (get) to see if an object already exists with the same name, if not, create a Congress Person Object
        congressPerson, created = CongressPerson.objects.get_or_create(fullName=name)
        
        # return the congressPerson object
        return congressPerson

    except Exception as e:
        # Error checking for possible errors as we gradually scale our database
        logging.error("Error while creating a congress person object")
        logging.error(e)

        # Do not add the transaction to the database if we dont know who it belongs to. Log the data and review the edge case later.
        return None

# Update Database
# Parameter: data (json)
def updateDB(data):
    congressTradesObjs = []

    for i, row in enumerate(data):
        # Get all values in a variable
        name = row['Name']

        # convert dates into proper format
        notificationDate = datetime.datetime.strptime(row['Notification Date'], '%m/%d/%Y').strftime('%Y-%m-%d')
        transactionDate = datetime.datetime.strptime(row['Transaction Date'], '%m/%d/%Y').strftime('%Y-%m-%d')
        
        # Assign variables to json items
        source = row['Link']
        ticker = row['Ticker']
        owner = row['Owner']
        assetDescription = row['Asset Name']
        assetType = row['Asset Type']
        transactionType = row['Type']
        amount = row['Amount']
        comment = row['Comment']

        # check if assetName contains a list
        assetDetails = None

        # If the assetDescription contains a list then we know that it contins extra details about the asset
        # For example option or bonds information
        if type(assetDescription) == list:
            # Check for Rates/Matures, and Options details
            if "Rates/Matures" in assetDescription[1][0].lower() or "put" in assetDescription[1][0].lower() or "call" in assetDescription[1][0].lower():
                # If it containd options or bonds information, flatten the list and add it to the assetDetails field
                assetDetails = " ".join(assetDescription[1])
            
            # if there is a list, the first element in the assetDescritions will contain the assetDescription 
            assetDescription = assetDescription[0]

        # get or create Ticker object
        ticker = getTicker(ticker[0])

        # get or create the congressperson object
        congressPerson = getCongressPerson(name)

        # Create Congress Trade Object and add it to objs
        try:
            congressTradesObjs.append(
                CongressTrade(
                    name=congressPerson,
                    ticker=ticker, 
                    transactionDate=transactionDate, 
                    disclosureDate=notificationDate, 
                    transactionType=transactionType, 
                    amount=amount, 
                    owner=owner, 
                    assetDescription=assetDescription, 
                    assetDetails=assetDetails,
                    assetType=assetType, 
                    comment=comment, 
                    pdf=False, 
                    ptrLink=source
                )
            )            
                
        except Exception as e:
            # Error checking for possible errors as we gradually scale our database

            # There is an overlap in dates, so a UNIQUE constraint error will be thrown, but should be ignored
            logging.error("Error while creating a congress trade object")
            logging.error(e)
            continue
    
    # Bulk create all the objects
    CongressTrade.objects.bulk_create(congressTradesObjs, ignore_conflicts=True)

# update all the ticker objects
def updateTickerStats():
    # Get all the tickers objects
    tickerObjs = Ticker.objects.all()
    # loop through all the tickers objects
    for ticker in tickerObjs:   
        # update each tickers stats
        ticker.updateStats()

# update all the congressperson objects
def updateCongressPersonStats():
    # Get all the congressperson objects
    congressPersonObjs = CongressPerson.objects.all()
    # loop through all the congressperson objects
    for congressPerson in congressPersonObjs:
        # update each congressperson stats
        congressPerson.updateStats()

def historical():
    # Load historical data  
    data = json.load(open("./congress/scripts/data/transactions.json"))
    updateDB(data)
    
    # Update the CongressPerson and Ticker summary stats 
    updateTickerStats()
    updateCongressPersonStats()

def current():
    # use senators script to get current data  
    
    # get todays date and format to month/day/year as thats the only format the API accepts
    today = datetime.datetime.today().strftime('%m-%d-%Y')
    
    # get data from API
    # data = getSenatorData(today)
    data = getSenatorData('1/1/2022')
    
    # call update database function
    updateDB(data)

    # Update the CongressPerson and Ticker summary stats 
    updateTickerStats()
    updateCongressPersonStats()
