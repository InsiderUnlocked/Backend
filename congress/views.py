# Import Libraries
from django_filters.rest_framework import DjangoFilterBackend
# Import Libraries
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import filters
from .serializers import CongressPersonSerializer, CongressTradeSerializer, SummaryStatSerializer, TickerSerializer
from .models import CongressPerson, CongressTrade, Ticker, SummaryStat

from django.core.management import call_command
from django.db.models import Q
import datetime

# TODO: Remove this in production
from .scripts.congressPeople import main as updateCongressPersonMain
from .populate import historical as historicalPopulate
from .populate import current as currentPopulate


import logging

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
    


# government/congress-trades endpoint
# Returns all of the Congress Transactions
class AllCongressViewSet(viewsets.ModelViewSet):
    # Permission needed to access endpoint
    permission_classes = (permissions.AllowAny,)
    
    # Querying database to get all the transactions
    queryset = CongressTrade.objects.all()

    # Serializing the data (converting to JSON)
    serializer_class = CongressTradeSerializer

    # Adding Logic to filter the data
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ticker__ticker', 'name__fullName', 'transactionType']
    search_fields = ['ticker__ticker', 'name__fullName', 'transactionType']
    # ordering_fields = ['ticker', 'name']
    ordering = ['-transactionDate']


# government/congress-all endpoint
# Returns all of the Congress Peoples Profiles who have made at least one transaction
class AllCongressPeopleViewSet(viewsets.ModelViewSet):
    # Permission needed to access endpoint
    permission_classes = (permissions.AllowAny,)
    # Convering the data to JSON
    serializer_class = CongressPersonSerializer
    # Querying database for all senators that have made at least one or more transactions
    queryset = CongressPerson.objects.filter(totalTransactions__gt=0).order_by('firstName')
    
    # Adding Logic to filter the data
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['fullName']
    search_fields = ['fullName']

# government/ticker endpoint
# Returns all of transactions that involved a specific ticker which is passed in the URL
class TickerViewSet(viewsets.ModelViewSet):
    # Permission needed to access endpoint
    permission_classes = (permissions.AllowAny,)
    # URL parameter passed into url that also exists in the CongressTrade and Ticker models 
    lookup_field = 'ticker'
    # Initiliazing our seializer class
    serializer_class = CongressTradeSerializer


    # filter by slug in url in django rest framework modelviewset
    def get_queryset(self):
        # Query Database for the ticker id  
        ticker = Ticker.objects.get(ticker=self.kwargs['ticker'])
               
        transactionType = self.request.query_params.get('transactionType')
        keywords = self.request.query_params.get('name')
        
        queryset = CongressTrade.objects.filter(ticker=ticker) 
        
        if len(keywords) > 0:
            queryset = queryset.filter(name__fullName__icontains=keywords)        

        if len(transactionType) > 0:
            queryset = queryset.filter(transactionType=transactionType)    

        return queryset.order_by('-transactionDate')

    # Serialize and Paginate the data    
    def retrieve(self, request, *args, **kwargs):
        # Get the queried data
        result = self.get_queryset()

        # Paginate the data
        result_page = self.paginate_queryset(result)
        
        # Serialize the data - (convert to JSON)
        serializer = CongressTradeSerializer(result_page, many=True)
        
        return self.get_paginated_response(serializer.data)
# government/congress-trades endpoint
# Returns all of the Congress Transactions
class CongressPersonViewSet(viewsets.ModelViewSet):

    # Permission needed to access endpoint
    permission_classes = (permissions.AllowAny,)
    # URL parameter passed into url that also exists in the CongressTrade and CongressPerson models 
    lookup_field = 'name'
    # Initiliazing our seializer class
    serializer_class = CongressTradeSerializer
        
    # filter by slug in url in django rest framework modelviewset
    def get_queryset(self):
        # Get the name that was passed in the URL
        name = self.kwargs['name']
        ticker = self.request.query_params.get('ticker')

        # Parse slug into first and last name
        firstName = name.split()[0]
        lastName = name.split()[-1]

        # Get the id of the congress person passed into the URL 
        # Django Search-Bar-Like Functionality to match a name to a congress person object from the database
        # https://docs.djangoproject.com/en/dev/ref/contrib/admin/#django.contrib.admin.ModelAdmin.search_fields
        congressPerson = CongressPerson.objects.filter(fullName__icontains=name).first()
        # Get all transactions by congress person
        queryset = CongressTrade.objects.filter(name=congressPerson)
    
        if len(ticker) > 0:
            queryset = queryset.filter(ticker__ticker__icontains=ticker)

        return queryset

    # Serialize and Paginate the data    
    def retrieve(self, request, *args, **kwargs):
        # Get the queried data
        result = self.get_queryset()

        # Paginate the data
        result_page = self.paginate_queryset(result)
        
        # Serialize the data - (convert to JSON)
        serializer = CongressTradeSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)


class TickerStatsViewSet(viewsets.ModelViewSet):
# Permission needed to access endpoint
    permission_classes = (permissions.AllowAny,)
    # URL parameter passed into url that also exists in the CongressTrade and CongressPerson models 
    lookup_field = 'ticker'
    # Initiliazing our seializer class
    serializer_class = TickerSerializer
    
    # filter by slug in url in django rest framework modelviewset
    def get_queryset(self):
        ticker = self.kwargs['ticker']

        queryset = Ticker.objects.filter(ticker=ticker)

        return queryset 
    
    
   # Serialize and Paginate the data    
    def retrieve(self, request, *args, **kwargs):
        # Get the queried data
        result = self.get_queryset()

        # Paginate the data
        result_page = self.paginate_queryset(result)
        
        # Serialize the data - (convert to JSON)
        serializer = TickerSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)

class CongressStatsViewSet(viewsets.ModelViewSet):
# Permission needed to access endpoint
    permission_classes = (permissions.AllowAny,)
    # URL parameter passed into url that also exists in the CongressTrade and CongressPerson models 
    lookup_field = 'fullName'
    # Initiliazing our seializer class
    serializer_class = CongressPersonSerializer
    
    # filter by slug in url in django rest framework modelviewset
    def get_queryset(self):
        name = self.kwargs['fullName']

        # Parse slug into first and last name
        firstName = name.split()[0]
        lastName = name.split()[-1]

        # Get the id of the congress person passed into the URL 
        queryset = CongressPerson.objects.filter(fullName__icontains=firstName, lastName__icontains=lastName)
        print(queryset)

        return queryset 

    # Serialize and Paginate the data    
    def retrieve(self, request, *args, **kwargs):
        # Get the queried data
        result = self.get_queryset()

        # Paginate the data
        result_page = self.paginate_queryset(result)
        
        # Serialize the data - (convert to JSON)
        serializer = CongressPersonSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)


# government/summary-stats endpoint
class SummaryStatsViewSet(viewsets.ModelViewSet):
    # Permission needed to access endpoint
    permission_classes = (permissions.AllowAny,)
    # URL parameter passed into url that also exists in the CongressTrade and CongressPerson models 
    lookup_field = 'timeframe'
    # Initiliazing our seializer class
    serializer_class = SummaryStatSerializer
    
    # filter by slug in url in django rest framework modelviewset
    def get_queryset(self):
        timeframe = self.kwargs['timeframe']

        queryset = SummaryStat.objects.filter(timeframe=timeframe)

        return queryset


    # Serialize and Paginate the data    
    def retrieve(self, request, *args, **kwargs):
        # Get the queried data
        result = self.get_queryset()

        # Paginate the data
        result_page = self.paginate_queryset(result)
        
        # Serialize the data - (convert to JSON)
        serializer = SummaryStatSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)