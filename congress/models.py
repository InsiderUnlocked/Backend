# @Author Farhan Rehman
# Purpose: Initilze the table models for all our endpoints

# Imports 
from django.db.models import signals
from django.db import models

from .signals import summaryStatUpdate, tickerStatUpdate, congressPersonStatUpdate

from jsonfield import JSONField
import datetime

# Calculate the average colume of trades
# The transactions parameter accepts a queryset object of congress trade transactions 
def getSumMid(transactions):
    # Initialize the min and max sum values. These will keep track of our highest and lowest volumes possible. With this we can get the average volume.
    sumMin = 0
    sumMax = 0

    # Count the number of transactions
    total = transactions.count()

    # Hashmap of fixed price ranges matched their integer representations
    listOfAmounts = {
        "$1,001 - $15,000": (1001, 15000),
        "$15,001 - $50,000": (15001, 50000),
        "$50,001 - $100,000": (50001, 100000),
        "$100,001 - $250,000": (100001, 250000),
        "$250,001 - $500,000": (250001, 500000),
        "$500,001 - $1,000,000": (500001, 1000000),
        "$1,000,001 - $5,000,000": (1000001, 5000000),
        "$5,000,001 - $25,000,000": (5000001, 25000000),
        "$25,000,001 - $50,000,000": (25000001, 50000000),
        "Over $50,000,000": (50000000, 50000000),
    }

    # iterate through the amount of each transaction 
    # O(N) iteration on this loop through use of hashmap (Improved from previous O(N^2) iteration which used a nested for loop and array to search for the values)
    for i in range(total):
        # get the amount of the transaction using hashmap, and add the min value to sumMin and the max value to sumMax
        sumMin += listOfAmounts[str(transactions[i].amount)][0]
        sumMax += listOfAmounts[str(transactions[i].amount)][1]
    
    # Calculate the average traded volume using the max and min amount traded
    sumMid = (sumMax + sumMin) / 2

    # Return the average traded volume as a float
    return sumMid

# Names of Congress
class CongressPerson(models.Model):
    # bioguide
    # A CharField is a character field
    # max_length is the maximum number of characters
    # unique is a boolean value that determines if the field is unique

    # bioguide = models.CharField(max_length=100, unique=True)
    # # first name
    # firstName = models.CharField(max_length=1000)
    
    # # last name
    # lastName = models.CharField(max_length=1000)
    
    # full name
    fullName = models.CharField(max_length=1000, unique=True)
    
    # current party
    currentParty = models.CharField(max_length=100) 
    
    # current chamber
    currentChamber = models.CharField(max_length=100)
    
    # current state
    currentState = models.CharField(max_length=100)
    
    # congress person image
    image = models.CharField(max_length=10000)
    
    # terms
    # JSONField is a field that can store a JSON object
    # default is the default value of the field, which we set to as None
    # blank is a boolean value which indicates if a field can be blank ("")
    # null is a boolean value which indicates if a field can be null (None)
    termsServed = models.JSONField(default=None, blank=True, null=True)
    
    # total transactions
    # An integer field hold a integer of max value 2147483647
    totalTransactions = models.IntegerField(default=0)

    # Total Volume of transactions
    totalVolumeTransactions = models.IntegerField(blank=True, null=True, default=0)

    # purchase
    purchases = models.IntegerField(blank=True, null=True, default=0)
    # sales
    sales = models.IntegerField(blank=True, null=True, default=0)

    # String representation of object
    # Example without function below: <QuerySet [<Blog:>,<Blog:>,<Blog:>....]
    # Example with function below:  <QuerySet [<Blog:itsName>,<Blog:itsName>,<Blog:itsName>....]
    def __str__(self):
        return self.fullName

    # Update congress persons transaction count every time the object is saved 
    def updateStats(self):
        # Query database for all transactions for this congress person
        transactions = CongressTrade.objects.filter(name=self)

        # update model
        CongressPerson.objects.filter(fullName=self.fullName).update(
            # Count number of transactions
            totalTransactions=transactions.count(),
            purchases=transactions.filter(transactionType='Purchase').count(), 
            # Calculate the number of Sales
            # Here we use "startswith" because we have two options: "Sale (Full)" and "Sale (Partial)". Both of those options start with "Sale"
            sales=transactions.filter(transactionType__startswith='Sale').count(),
            # Calculate the total volume of transactions
            totalVolumeTransactions=getSumMid(transactions), 
        )
        
# Signals to update total transactions for each congress member when there has beed a save(post_save) or deletion(post_delete)
signals.post_save.connect(congressPersonStatUpdate, sender=CongressPerson)
signals.post_delete.connect(congressPersonStatUpdate, sender=CongressPerson)

# Tickers Tables
class Ticker(models.Model):
    # stock ticker
    ticker = models.CharField(max_length=100, unique=True)
    
    # company name 
    company = models.CharField(max_length=1000, null=True)

    # marketcap 
    # Big Integer Field is a field that can store a large integer value (the regular integerfields can only hold max 2147483647, and we need to store bigger values for a stocks marketcap)
    marketcap = models.BigIntegerField(blank=True, null=True)
    # sector
    sector = models.CharField(max_length=1000, null=True)
    # industry
    industry = models.CharField(max_length=1000, null=True)

    # Signals to update total transactions for each congress member
    # total transactions it occured in
    totalTransactions = models.IntegerField(blank=True, null=True, default=0)

    # Total Volume of transactions
    totalVolumeTransactions = models.IntegerField(blank=True, null=True, default=0)

    # Trade Type Ratio
    purchases = models.IntegerField(blank=True, null=True, default=0)
    sales = models.IntegerField(blank=True, null=True, default=0)
    
    # String representation of object
    # Example without function below: <QuerySet [<Blog:>,<Blog:>,<Blog:>....]
    # Example with function below:  <QuerySet [<Blog:itsName>,<Blog:itsName>,<Blog:itsName>....]
    def __str__(self):
        return self.ticker

    # Update congress persons transaction count every time the object is saved 
    def updateStats(self):
        # Query database for all transactions for this stock ticker
        transactions = CongressTrade.objects.filter(ticker=self)

        # update model
        try:
            Ticker.objects.filter(ticker=self).update(
                # Count number of transactions
                totalTransactions=transactions.count(), 
                # Calculate the number of purchases 
                purchases=transactions.filter(transactionType='Purchase').count(), 
                # Calculate the number of Sales
                # Here we use "startswith" because we have two options: "Sale (Full)" and "Sale (Partial)". Both of those options start with "Sale"
                sales=transactions.filter(transactionType__startswith='Sale').count(),
                # Calculate the total volume of transactions
                totalVolumeTransactions=getSumMid(transactions), 
            )
        except Exception as e:
            print("ERROR: ", str(e))
    

# Signals to update total transactions for each congress member
signals.post_save.connect(tickerStatUpdate, sender=Ticker)
signals.post_delete.connect(tickerStatUpdate, sender=Ticker)
    
# Combination of Senator and House Data
class CongressTrade(models.Model):
    # Foreign KEY (connect to another table with congress persons names, see ERD Diagram in InsiderUnlocked/Insider-Unlocked for more information)
    name = models.ForeignKey(CongressPerson, on_delete=models.CASCADE)
    
    # Foreign KEY (connect to another table with ticker name, see ERD Diagram in InsiderUnlocked/Insider-Unlocked for more information)
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE, null=True)

    # transaction date
    # A DateField is a field that can store a date value
    transactionDate = models.DateField(blank=True, null=True)
    
    # disclosure date
    # A DateField is a field that can store a date value
    disclosureDate = models.DateField(blank=True, null=True)

    # transaction type
    transactionType = models.CharField(max_length=60, blank=True)
    
    # amount spent (this is a range)
    amount = models.CharField(max_length=60, blank=True)
    
    # owner of transaction (spouce, child, etc)
    owner = models.CharField(max_length=60)

    # asset description
    assetDescription = models.CharField(max_length=1000, blank=True)
    
    # asset details
    assetDetails = models.CharField(max_length=1000, blank=True, null=True)

    # asset type (Stock, Bond)
    assetType = models.CharField(max_length=1000, blank=True)

    # source link
    ptrLink = models.CharField(max_length=100)
    
    # comment
    comment = models.CharField(max_length=1000, blank=True)
    
    # is the transaction a pdf
    # A BooleanField is a field that can store a boolean value
    pdf = models.BooleanField()
    
    # String representation of object
    # Example without function below: <QuerySet [<Blog:>,<Blog:>,<Blog:>....]
    # Example with function below:  <QuerySet [<Blog:itsName>,<Blog:itsName>,<Blog:itsName>....]
    def __str__(self):
        return self.name.fullName
    
    # Class we can use in django to create a unique_together constraint (can only create fields if they have a different value that an existing one combined with the fields listed), and ordering (orders the trades done by congress by the transaction date)
    class Meta:
        unique_together = ('disclosureDate', 'transactionDate', 'owner', 'ticker', 'assetDescription', 'assetType', 'transactionType', 'amount', 'comment', 'name', 'pdf', 'ptrLink')
        ordering = ["-transactionDate"]


# Summary of all transactions 
class SummaryStat(models.Model):
    total = models.BigIntegerField(default=0)
    purchases = models.BigIntegerField(default=0)
    sales = models.BigIntegerField(default=0)
    totalVolume = models.BigIntegerField(default=0)
    timeframe = models.BigIntegerField(unique=True)
    
    # String representation of object
    # Example without function below: <QuerySet [<Blog:>,<Blog:>,<Blog:>....]
    # Example with function below:  <QuerySet [<Blog:itsName>,<Blog:itsName>,<Blog:itsName>....]
    def __str__(self):
        return str(self.total)
            
    # Class we can use in django to create a unique_together constraint (can only create fields if they have a different value that an existing one combined with the fields listed), and ordering (orders the trades done by congress by the transaction date)
    class Meta:
        unique_together = ('total', 'purchases', 'sales', 'totalVolume', 'timeframe',)

    # Update congress persons transaction count every time the object is saved 
    def updateStats(self):
        # Query database for all transactions for this congress person
        transactions = CongressTrade.objects.filter(transactionDate__lte=datetime.datetime.today(), transactionDate__gt=datetime.datetime.today()-datetime.timedelta(days=self.timeframe))

        # update model
        SummaryStat.objects.filter(id=self.id).update(
            # Count number of transactions
            total=transactions.count(), 
            # Count number of transactions
            purchases=transactions.filter(transactionType='Purchase').count(), 
            # Calculate the number of Sales
            # Here we use "startswith" because we have two options: "Sale (Full)" and "Sale (Partial)". Both of those options start with "Sale"
            sales=transactions.filter(transactionType__startswith='Sale').count(),
            # Calculate the total volume of transactions
            totalVolume=getSumMid(transactions), 
        )

# Signals to update total transactions for each congress member
signals.post_save.connect(summaryStatUpdate, sender=SummaryStat)
signals.post_delete.connect(summaryStatUpdate, sender=SummaryStat)
