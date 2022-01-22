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
        # If the ticker is equal to "--", then return None as it means the asset type is not a stock 
        if stockTicker == "--":
            return None

        # Check to see if the stock ticker is already in the database, if not, create it
        # tickerObj holds the object
        # created is a boolean value which indicates if the object has been created or not
        tickerObj, created = Ticker.objects.get_or_create(ticker=stockTicker)

        # If the stock ticker has just beed created
        if created == True:
            # Get more data about the stock ticker
            sector, industry, company, marketcap = getTickerData(stockTicker)
            
            # Assign the stock ticker information to the newly created ticker object 
            tickerObj.sector = sector
            tickerObj.industry = industry
            tickerObj.company = company
            tickerObj.marketcap = marketcap
            
            # Save the changes to the database
            tickerObj.save()
        
        return tickerObj
    except Exception as e:
        logging.error("Error while creating a stock ticker object")
        logging.error(e)


# Get or Create Congress Person Object
# Parameter: name (string)
def getCongressPerson(name):
    try:
        # find congress person object in database table CongressPerson
        # "Collins, Susan M. (Senator)" --> "Susan M. Collins"
        name = name.replace(" (Senator)", "")

        # add everything before the comma to everything after the comma
        name =  name.split(',')[-1] + " " + name.split(',')[0]

        # remove trailing whitespace
        name = name.strip()

        # get the first and last name by 
        firstName = name.split()[0]
        lastName = name.split()[-1]

        # Django Search-Bar-Like Functionality to match a name to a congress person object from the database
        # https://docs.djangoproject.com/en/dev/ref/contrib/admin/#django.contrib.admin.ModelAdmin.search_fields
        congressPerson = CongressPerson.objects.filter(
            Q(fullName__icontains=name) | 
            Q(firstName__icontains=name) | 
            Q(lastName__icontains=name) |

            Q(fullName__icontains=firstName) | 
            Q(firstName__icontains=firstName) | 
            Q(lastName__icontains=firstName) |

            Q(fullName__icontains=lastName) | 
            Q(firstName__icontains=lastName) | 
            Q(lastName__icontains=lastName)
        ).first()

    except Exception as e:
        logging.error("Error while creating a congress person object")
        logging.error(e)
        # Do not add the transaction to the database if we dont know who it belongs to. Log the data and review the edge case later.
        return None

# Update Database
# Parameter: data (json)
def updateDB(data):

    for row in data:
        # Get all values in a variable
        name = row['Name']

        # convert dates into proper format
        notificationDate = datetime.datetime.strptime(row['Notification Date'], '%m/%d/%Y').strftime('%Y-%m-%d')
        transactionDate = datetime.datetime.strptime(row['Transaction Date'], '%m/%d/%Y').strftime('%Y-%m-%d')
        
        source = row['Link']
        ticker = row['Ticker']
        owner = row['Owner']
        assetDescription = row['Asset Name']
        assetType = row['Asset Type']
        transactionType = row['Type']
        amount = row['Amount']
        comment = row['Comment']

        # check if assetName contains a list
        if type(assetDescription) == list:
            # Check for Rates/Matures, and Options details
            if "Rates/Matures" in assetDescription[1][0].lower() or "put" in assetDescription[1][0].lower() or "call" in assetDescription[1][0].lower():
                # assetDetails = assetDescription[1][0]
                assetDetails = " ".join(assetDescription[1])
            
            else:
                assetDetails = None
            
            assetDescription = assetDescription[0]

        # Create Ticker if theres a ticker
        ticker = getTicker(ticker[0])
        congressPerson = getCongressPerson(name)

        # Create Congress Trade Object and add it to objs
        try:
            CongressTrade.objects.get_or_create(
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
            # update congress person object
            congressPerson.updateStats()
            ticker.updateStats()

        except Exception as e:
            # There is an overlap in dates, so a UNIQUE constraint error will be thrown, but should be ignored
            logging.error("Error while creating a congress trade object")
            logging.error(e)
            continue

def historical():
    # Load historical data  
    data = json.load(open("./congress/scripts/data/transactions.json"))
    updateDB(data)

def current():
    # use senators script to get current data  
    
    # get todays date and format to month/day/year as thats the only format the API accepts
    today = datetime.datetime.today().strftime('%m-%d-%Y')
    
    # get data from API
    data = getSenatorData(today)
    
    # call update database function
    updateDB(data)
