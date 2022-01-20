# Purpose: This file will scrape data from the Senate website and return the data asJSON 

# Import Libraries
from .cleanText import cleanText
from bs4 import BeautifulSoup
import pandas as pd
import requests
import logging
import math
import json
import time

# Intialize Constant URL variables
global homeURL
homeURL = "https://efdsearch.senate.gov/search/home/"

global searchURL
searchURL = "https://efdsearch.senate.gov/search/report/data/"

global reportURL
reportURL = "https://efdsearch.senate.gov/search/report/data/"

global prefixURL 
prefixURL = "https://efdsearch.senate.gov"

global session
session = requests.Session() 

global tableData
tableData = []

# BYPASS TERMS OF SERVICE PAGE 
'''
When a person clicks the checkbox, the website sends a request to the server side validating CSRF token, so in our case we send the request ourself with our CSRF token which is given as a cookie in the beginning of the website  
Collect validated CSRF token through the cookies of the website.

Once we validate the CSRF token we store in a variable so that we can have a validated CSRF token to implement future requests.
'''
def bypassTOS():    
    try:
        # Get unvalidated CSRF token from cookies
        response = session.get(homeURL)
        csrfToken = session.cookies['csrftoken']

        # Valitate CSRF token by sending CSRF token and { 'prohibition_agreement': 1 } to the server agree to the TOS (Terms of Service) and validate our CSRF token 
        payload = { 'csrfmiddlewaretoken': csrfToken, 'prohibition_agreement': 1 }
        response = session.post(homeURL, data=payload, headers={'Referer': homeURL})

        # Retreive validated CSRF token
        csrfToken = session.cookies['csrftoken']

        return csrfToken
    except Exception as e:
        logging.error("Error in bypassTOS function: " + e)
        raise e



# GET REPORTS BASED ON FILTERS 
'''
Open search page
Search for data based specific filters
Send a request to the resulting table 
# Using the validated CSRF we can send a request to the search page, with a payload attached with all the preferred filters

Going through all the pages of the table, the table is paginated iteratively
# If there are is more than one page in the table we have to detect that and iterate through all the pages(POSSIBLY recursively)
'''
def getReports(csrfToken, start, reportType, startDate, lastName):    
    try:
        payload = {
            'start': str(start),
            'report_types': f'[{reportType}]',
            'submitted_start_date': f'{startDate} 00:00:00',
            'last_name': lastName,
            'length': 100,
            'csrfmiddlewaretoken': csrfToken
        }

        # Send request to and store the response
        response = session.post(reportURL, data=payload, headers={'Referer': homeURL})
        
        # load the response as json
        jsonResponse = response.json()
        records = jsonResponse['data']

        # loop through the data
        for record in records:
            # get the name from record array. The name will always be the second index in the array
            name = record[2]
            # get the link from the array. The link will always be the third index in the array
            link = record[3]
            # get the notification date from the array. The notification date  will always be the foruth index in the array
            notificationDate = record[4] 

            # slicing the string to only get the url from href tag in the HTML
            link = link[ link.find('="')+2 : link.find('" t') ]

            # send informatio to parseHTML function to get the transaction data
            parseHTML(csrfToken, link, name, notificationDate)
        
        # Calculate the number of pages in the table and round it the next highest 100
        numOfPages = math.ceil(jsonResponse['recordsTotal'] / 100) * 100
        
        # recurisvely go through all the pages until we reach the last page
        if start != numOfPages:
            return getReports(csrfToken, start+100, reportType, startDate, lastName)
    except Exception as e:
        logging.error("Error in getReports function: " + e)
        raise e
    
    

# SCRAPE DATA FROM EACH RECORD
'''
loop through each row in table
	Open the link in each row which returns a html file

Scrape all the data from the from each row iteratively as well 
## We retrieve the html page from the previous request and parse the html file for a table
## Than we iterate through the table and store each row in our local database
'''

# PARSE PERIODIC TRANSAACTION REPORT HTML PAGE
def parseHTML(csrfToken, link, name, notificationDate):
    try:
        if "paper" in link:
            # This means that the link is a pdf report and thus unscrapable
            return False
        
        # Send request to link with our CSRF token, and retrieve the html file    
        payload = {
            'csrfmiddlewaretoken': csrfToken
        }
        
        url = prefixURL + link
        response = session.post(url, data=payload, headers={'Referer': reportURL})

        # Parse HTML
        parsedData = BeautifulSoup(response.text, 'html.parser')

        # Get the table
        table = parsedData.find('table')

        # Get the rows from the table
        rows = table.find_all('tr')

        # Add all the periodic transaction data to this list
        # tableData = []

        # iterate through the rows
        for i, row in enumerate(rows):
            # we do not have to scrape the first row so we can ignore this iteration
            if i == 0:
                continue
        
            # find all the table data
            tds = row.find_all("td")

            # Store the rows data within this list. We want each periodic transaction to include the name, notificationDate, and url, and since we already have that data at this point, we will add them to the list
            rowData = [name, notificationDate, url]
            
            # iterate through the table data
            for i, td in enumerate(tds):
                # Do not record data from the first column we can ignore this iteration
                if i == 0:
                    continue
                # If the ticker column contains a stock ticker, it also has a link to that stock on yahoo fiannce
                if i == 3:
                    # check to see if theres an a tag in the table
                    if td.find('a') != None:
                        link = td.find('a')
                        rowData.append([link.text, link.get('href')])
                    else:
                        #if there isnt clean the text
                        rowData.append(cleanText(td.text.strip()))
                # If the Asset Name column contains extra text in nested div, collect that information
                elif i == 4:
                    # check to see if theres a div tag in the td
                    if td.find('div') != None:
                        # asset name
                        mainText = td.contents[0].strip()
                        #
                        subtext = td.find_all( 'div', {'class': 'text-muted'} )
                        subtextArray = []

                        for i in subtext:
                            subtextArray.append(cleanText(i.text.strip()))

                        rowData.append([mainText, subtextArray])
                    else:
                        rowData.append(cleanText(td.text.strip()))
                else:
                    rowData.append(cleanText(td.text.strip()))


            # tableData.append(rowData)
            tableData.append(rowData)
        

        # Avoid rate limit on website by delaying the program for two seconds
        time.sleep(2)
    except Exception as e:
        logging.error('Error occured in the parseHTML function: ' + e)
        print(link)
        raise e


def main(startDate):
    # Get validated CSRF token
    CSRF = bypassTOS()
    
    # Filters for Get Reports
    start = 0
    # Report Type 11 means the "periodic transactions" filter
    reportType = 11
    # startDate = "01/01/2012"
    lastName = ''

    # Get Reports
    records = getReports(CSRF, start, reportType, startDate, lastName)



    df = pd.DataFrame(tableData, columns =['Name', 'Notification Date', 'Link', 'Transaction Date', 'Owner', 'Ticker', 'Asset Name', 'Asset Type', 'Type', 'Amount', 'Comment']) 

    # pandas dataframe to json
    dfJson = df.to_json(orient='records')
    parsedJson = json.loads(dfJson)

    # outfile = open('transactions.json', 'a', encoding='utf-8')
    # outfile.write(json.dumps(parsedJson, ensure_ascii=False, indent=4))
    # # outfile.write(",\n")
    # outfile.close()
    
    return parsedJson

