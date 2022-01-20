# Purpose: Initilze the table models for all our endpoints
from django.db.models import signals
from .signals import tradesCount, summaryStatUpdate, tickerStatUpdate, congressPersonStatUpdate
from django.db import models
from jsonfield import JSONField
import datetime

# Names of Congress
class CongressPerson(models.Model):
    # bioguide
    bioguide = models.CharField(max_length=100, unique=True)
    # first name
    firstName = models.CharField(max_length=1000)
    
    # last name
    lastName = models.CharField(max_length=1000)
    
    # full name
    fullName = models.CharField(max_length=1000)
    
    # current party
    currentParty = models.CharField(max_length=100) 
    
    # current chamber
    currentChamber = models.CharField(max_length=100)
    
    # current state
    currentState = models.CharField(max_length=100)
    
    # congress person image
    image = models.CharField(max_length=10000)
    
    # terms
    termsServed = models.JSONField(default=None, blank=True, null=True)
    
    # total transactions
    totalTransactions = models.BigIntegerField(default=0)

    # Total Volume of transactions
    totalVolumeTransactions = models.BigIntegerField(blank=True, null=True, default=0)

    # Trade Type Ratio
    purchases = models.BigIntegerField(blank=True, null=True, default=0)
    sales = models.BigIntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return self.fullName

    # Update congress persons transaction count every time the object is saved 
    def updateStats(self):
        # transactions = CongressTrade.objects.filter(name=self, transactionDate__lte=datetime.datetime.today(), transactionDate__gt=datetime.datetime.today()-datetime.timedelta(days=90))
        transactions = CongressTrade.objects.filter(name=self)


        # Get the number of transactions by congress person
        total = transactions.count()

        # # Trade Type Ratio
        # self.purchases = transactions.filter(transactionType='Purchase').count()
        # self.sales = transactions.filter(transactionType__startswith='Sale').count()


        # Total Volume
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
        

        sumMin = 0
        sumMax = 0 

        # iterate through the amount of each transaction 
        # O(N) iteration on this loop through use of hashmap (Improved from previous O(N^2) iteration)))
        for i in range(total):
            # get the amount of the transaction using hashmap
            sumMin += listOfAmounts[str(transactions[i].amount)][0]
            sumMax += listOfAmounts[str(transactions[i].amount)][1]
        
        sumMid = (sumMax + sumMin) / 2

        # update model
        CongressPerson.objects.filter(bioguide=self.bioguide).update(
            totalTransactions=transactions.count(), 
            purchases=transactions.filter(transactionType='Purchase').count(), 
            sales=transactions.filter(transactionType__startswith='Sale').count(),
            totalVolumeTransactions=sumMid, 
        )
        
# Signals to update total transactions for each congress member
signals.post_save.connect(congressPersonStatUpdate, sender=CongressPerson)
signals.post_delete.connect(congressPersonStatUpdate, sender=CongressPerson)

# Tickers Tables
class Ticker(models.Model):
    # stock ticker
    ticker = models.CharField(max_length=100, unique=True)
    
    # company name 
    company = models.CharField(max_length=1000)

    # marketcap 
    marketcap = models.BigIntegerField(blank=True, null=True)
    # sector
    sector = models.CharField(max_length=1000)
    # industry
    industry = models.CharField(max_length=1000)

    # Signals to update total transactions for each congress member
    # total transactions it occured in
    totalTransactions = models.BigIntegerField(blank=True, null=True, default=0)

    # Total Volume of transactions
    totalVolumeTransactions = models.BigIntegerField(blank=True, null=True, default=0)

    # Trade Type Ratio
    purchases = models.BigIntegerField(blank=True, null=True, default=0)
    sales = models.BigIntegerField(blank=True, null=True, default=0)

    
    def __str__(self):
        return self.ticker


    # Update congress persons transaction count every time the object is saved 
    def updateStats(self):
        # transactions = CongressTrade.objects.filter(ticker=self, transactionDate__lte=datetime.datetime.today(), transactionDate__gt=datetime.datetime.today()-datetime.timedelta(days=90))
        transactions = CongressTrade.objects.filter(ticker=self)
        print(transactions)
        # Get the number of transactions by congress person
        total = transactions.count()

        # # Trade Type Ratio
        # self.purchases = transactions.filter(transactionType='Purchase').count()
        # self.sales = transactions.filter(transactionType__startswith='Sale').count()


        # Total Volume
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
        

        sumMin = 0
        sumMax = 0 

        # iterate through the amount of each transaction 
        # O(N) iteration on this loop through use of hashmap (Improved from previous O(N^2) iteration)))
        for i in range(total):
            # get the amount of the transaction using hashmap
            sumMin += listOfAmounts[str(transactions[i].amount)][0]
            sumMax += listOfAmounts[str(transactions[i].amount)][1]
        
        sumMid = (sumMax + sumMin) / 2

        # update model
        try:
            Ticker.objects.filter(ticker=self).update(
                totalTransactions=transactions.count(), 
                purchases=transactions.filter(transactionType='Purchase').count(), 
                sales=transactions.filter(transactionType__startswith='Sale').count(),
                totalVolumeTransactions=sumMid, 
            )
        except Exception as e:
            print("ERROR: ", str(e))

# Signals to update total transactions for each congress member
signals.post_save.connect(tickerStatUpdate, sender=Ticker)
signals.post_delete.connect(tickerStatUpdate, sender=Ticker)
    
# Combination of Senator and House Data
class CongressTrade(models.Model):
    # PRIMARY KEY (connect to another table with congress persons names)
    name = models.ForeignKey(CongressPerson, on_delete=models.CASCADE)
    
    # PRIMARY KEY (connect to another table with ticker name)
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE, null=True)

    # transaction date
    transactionDate = models.DateField(blank=True, null=True)
    
    # disclosure date
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
    pdf = models.BooleanField()
    

    def __str__(self):
        return self.name.fullName
    

    # class Meta:
    #     unique_together = ('disclosureDate', 'transactionDate', 'owner', 'ticker', 'assetDescription', 'assetType', 'transactionType', 'amount', 'comment', 'name', 'pdf', 'ptrLink')
    #     ordering = ["-transactionDate"]


# Summary of all transactions 
class SummaryStat(models.Model):
    total = models.BigIntegerField(default=0)
    purchases = models.BigIntegerField(default=0)
    sales = models.BigIntegerField(default=0)
    totalVolume = models.BigIntegerField(default=0)
    timeframe = models.BigIntegerField(unique=True)
    
    def __str__(self):
        return str(self.total)
            
    class Meta:
        unique_together = ('total', 'purchases', 'sales', 'totalVolume', 'timeframe',)
        # ordering = ["-transactionDate"]

    # Update congress persons transaction count every time the object is saved 
    def updateStats(self):
        transactions = CongressTrade.objects.filter(transactionDate__lte=datetime.datetime.today(), transactionDate__gt=datetime.datetime.today()-datetime.timedelta(days=90))

        # Get the number of transactions by congress person
        total = transactions.count()

        # # Trade Type Ratio
        # self.purchases = transactions.filter(transactionType='Purchase').count()
        # self.sales = transactions.filter(transactionType__startswith='Sale').count()


        # Total Volume
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
        

        sumMin = 0
        sumMax = 0 

        # iterate through the amount of each transaction 
        # O(N) iteration on this loop through use of hashmap (Improved from previous O(N^2) iteration)))
        for i in range(total):
            # get the amount of the transaction using hashmap
            sumMin += listOfAmounts[str(transactions[i].amount)][0]
            sumMax += listOfAmounts[str(transactions[i].amount)][1]
        
        sumMid = (sumMax + sumMin) / 2

        # update model
        SummaryStat.objects.filter(id=self.id).update(
            total=transactions.count(), 
            purchases=transactions.filter(transactionType='Purchase').count(), 
            sales=transactions.filter(transactionType__startswith='Sale').count(),
            totalVolume=sumMid, 
        )

# Signals to update total transactions for each congress member
signals.post_save.connect(summaryStatUpdate, sender=SummaryStat)
signals.post_delete.connect(summaryStatUpdate, sender=SummaryStat)
