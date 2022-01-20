# Purpose: This script is used to download the current and historical members of the US Congress

# Import Libraries
from ..models import CongressPerson
import requests
import json

# Intialize Constant URL variables
global currentMembersURL
currentMembersURL = "https://theunitedstates.io/congress-legislators/legislators-current.json"

global historicalMembersURL
historicalMembersURL = "https://theunitedstates.io/congress-legislators/legislators-historical.json"

# turn response into json
def getDetails(response):    
    objs = json.loads(response.text)
    # hashmap of states names
    states = {
        'AL': 'Alabama',
        'AK': 'Alaska',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'AR': 'Arkansas',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'IA': 'Iowa',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'ME': 'Maine',
        'MD': 'Maryland',
        'MA': 'Massachusetts',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MS': 'Mississippi',
        'MO': 'Missouri',
        'MT': 'Montana',
        'MP': 'Northern Mariana Islands',
        'NE': 'Nebraska',
        'NV': 'Nevada',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NY': 'New York',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VT': 'Vermont',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'WA': 'Washington',
        'WV': 'West Virginia',
        'WI': 'Wisconsin',
        'WY': 'Wyoming'
    }


    # initilize data variable to hold objects for bulk crete
    data = []

    for i in range(len(objs)):
        # if the object is a historical member, skip it we only care about 2012 - present cause that where the financial data is
        
        # Iterate through all terms and see if any terms end dates are 2008 or later
        for j in range(len(objs[i]['terms'])):
            # a Senators term length is 6 years. So we want to see if their end year greater than 2006, since data only started getting recorded from 2012 and onwards
            if int(objs[i]['terms'][j]["end"][:4]) < 2000:
                # skip iteration
                continue

        try:
            # get congress person bioguide ot be able to get the image
            bioguide = objs[i]["id"]["bioguide"]
            # get the image
            imageURL = f"https://theunitedstates.io/images/congress/225x275/{bioguide}.jpg"
            
            #make request to image url
            imageResponse = requests.get(imageURL)
            
            # if image is not found, set image to default
            if imageResponse.status_code != 200:
                imageURL = "data:image/jpeg;base64,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"

            firstName = objs[i]["name"]["first"]
            lastName = objs[i]["name"]["last"]
            
            # check if there is a full name object
            if "official_full" in objs[i]["name"]:
                fullName = objs[i]["name"]["official_full"]
            else:
                fullName = firstName + " " + lastName
            
            # get the sate
            state = states[objs[i]["terms"][-1]["state"]]

            #check if party is in the object
            if "party" in objs[i]["terms"][-1]:
                party = objs[i]["terms"][-1]["party"]
            else:
                party = "Unknown"

            # get the chamber
            chamber = "Senator" if objs[i]["terms"][-1]["type"] == "sen" else "House"
            
            termsServed = objs[i]["terms"]

            data.append(CongressPerson(bioguide=bioguide, firstName=firstName, lastName=lastName, fullName=fullName, currentState=state, currentParty=party, currentChamber=chamber, image=imageURL, termsServed=termsServed))
            print("done")
        except Exception as e:
            print(e)
            continue
    
    # bulk add data
    CongressPerson.objects.bulk_create(data, ignore_conflicts=True)

def getCurrentMembers():
    # download file as current-members.json
    response = requests.get(currentMembersURL)
    # with open('./data/currentCongress.json', 'w') as f:
    #     f.write(response.text)
    getDetails(response)    

def getHistoricalMembers():
    # download file as current-members.json
    response = requests.get(historicalMembersURL)
    # with open('./data/historicalCongress.json', 'w') as f:
    #     f.write(response.text)
    getDetails(response)    

def main():
    getCurrentMembers()
    getHistoricalMembers()

