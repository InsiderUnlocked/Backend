# @Author Farhan Rehman

# Imports
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import filters

from .serializers import CongressPersonSerializer, CongressTradeSerializer, SummaryStatSerializer, TickerSerializer
from .models import CongressPerson, CongressTrade, Ticker, SummaryStat

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
    # Filtering by ticker, full name, and transaction type (buy/sell)
    filterset_fields = ['ticker__ticker', 'name__fullName', 'transactionType']
    # Searching by ticker, full name, and transaction type (buy/sell)
    search_fields = ['ticker__ticker', 'name__fullName', 'transactionType']
    # Ordering by results by transaction date (newest first)
    ordering = ['-transactionDate']


# government/congress-all endpoint
# Returns all of the Congress Peoples Profiles who have made at least one transaction
class AllCongressPeopleViewSet(viewsets.ModelViewSet):
    # Permission needed to access endpoint
    permission_classes = (permissions.AllowAny,)
    # Convering the data to JSON
    serializer_class = CongressPersonSerializer
    # Querying database for all senators that have made at least one or more transactions
    queryset = CongressPerson.objects.filter(totalTransactions__gt=0).order_by('fullName')
    
    # Adding Logic to filter the data
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    # Filtering by full name
    filterset_fields = ['fullName']
    # Searching by full name
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
        # replace dashes in ticker with periods
        tickerStr = self.kwargs['ticker'].replace('-', '.')

        # Query Database for the ticker id  
        ticker = Ticker.objects.get(ticker=tickerStr)
        
        # accept transactions type and name parametes from the url in addition
        transactionType = self.request.query_params.get('transactionType')
        name = self.request.query_params.get('name')
        
        # Query Database for all transactions using the ticker id
        queryset = CongressTrade.objects.filter(ticker=ticker) 
        
        # Checks we need to run to see if we have a parameter for name
        if name is not None:
            if len(name) > 0:
                # Query Database for all transactions using the name
                # icontins is used to search for partial matches
                queryset = queryset.filter(name__fullName__icontains=name)        

        # Checks we need to run to see if we have a parameter for transactionType
        if transactionType is not None:
            if len(transactionType) > 0:
                # Query Database for all transactions depending on the transaction type
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
        
        # Return the serialized and paginated data
        return self.get_paginated_response(serializer.data)

# government/congress-trades endpoint
# Returns all of the Congress Transactions
class CongressPersonViewSet(viewsets.ModelViewSet):

    # Permission needed to access endpoint
    permission_classes = (permissions.AllowAny,)
    # URL parameter passed into url that also exists in the CongressTrade and CongressPerson models 
    lookup_field = 'fullName'
    # Initiliazing our seializer class
    serializer_class = CongressTradeSerializer
        
    # filter by slug in url in django rest framework modelviewset
    def get_queryset(self):
        # Get the name that was passed in the URL
        fullName = self.kwargs['fullName']

        # accept transactions type and name parametes from the url in addition
        transactionType = self.request.query_params.get('transactionType')
        ticker = self.request.query_params.get('ticker')

        # Query Database for the bioguide id
        congressPerson = CongressPerson.objects.get(fullName=fullName)

        # Get all transactions by congress person
        queryset = CongressTrade.objects.filter(name=congressPerson)
    
        # Checks we need to run to see if we have a parameter for ticker
        if ticker is not None:
            if len(ticker) > 0:
                # Replace any tickers with dashes with periods 
                # Since urls cant have perioids and tickers have them, we add dashes instead to pass them in the urls parameter. Then we replace them with periods here.
                ticker = ticker.replace('-', '.')
                # Query Database for all transactions using the ticker
                queryset = queryset.filter(ticker__ticker__icontains=ticker)

        # Checks we need to run to see if we have a parameter for transactionType
        if transactionType is not None:
            if len(transactionType) > 0:
                # Query Database for all transactions depending on the transaction type
                queryset = queryset.filter(transactionType=transactionType)

        return queryset

    # Serialize and Paginate the data    
    def retrieve(self, request, *args, **kwargs):
        # Get the queried data
        result = self.get_queryset()

        # Paginate the data
        result_page = self.paginate_queryset(result)
        
        # Serialize the data - (convert to JSON)
        serializer = CongressTradeSerializer(result_page, many=True)

        # Return the serialized and paginated data
        return self.get_paginated_response(serializer.data)

# government/ticker endpoint
class TickerStatsViewSet(viewsets.ModelViewSet):
# Permission needed to access endpoint
    permission_classes = (permissions.AllowAny,)
    # URL parameter passed into url that also exists in the CongressTrade and CongressPerson models 
    lookup_field = 'ticker'
    # Initiliazing our seializer class
    serializer_class = TickerSerializer
    
    # filter by slug in url in django rest framework modelviewset
    def get_queryset(self):
        # Get the ticker that was passed in the URL
        ticker = self.kwargs['ticker']

        # Query Database for the ticker by ticker name
        queryset = Ticker.objects.filter(ticker=ticker)

        # return queryset
        return queryset 
    
    
   # Serialize and Paginate the data    
    def retrieve(self, request, *args, **kwargs):
        # Get the queried data
        result = self.get_queryset()

        # Paginate the data
        result_page = self.paginate_queryset(result)
        
        # Serialize the data - (convert to JSON)
        serializer = TickerSerializer(result_page, many=True)

        # Return the serialized and paginated data
        return self.get_paginated_response(serializer.data)

# government/congress-stats
class CongressStatsViewSet(viewsets.ModelViewSet):
# Permission needed to access endpoint
    permission_classes = (permissions.AllowAny,)
    # URL parameter passed into url that also exists in the CongressTrade and CongressPerson models 
    lookup_field = 'fullName'
    # Initiliazing our seializer class
    serializer_class = CongressPersonSerializer
    
    # filter by slug in url in django rest framework modelviewset
    def get_queryset(self):
        fullName = self.kwargs['fullName']

        # Get the id of the congress person passed into the URL 
        queryset = CongressPerson.objects.filter(fullName=fullName)

        # return queryset
        return queryset 

    # Serialize and Paginate the data    
    def retrieve(self, request, *args, **kwargs):
        # Get the queried data
        result = self.get_queryset()

        # Paginate the data
        result_page = self.paginate_queryset(result)
        
        # Serialize the data - (convert to JSON)
        serializer = CongressPersonSerializer(result_page, many=True)

        # Return the serialized and paginated data
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
        # Get the timeframe that was passed in the URL
        timeframe = self.kwargs['timeframe']

        # Query Database for the timeframe by timeframe name
        queryset = SummaryStat.objects.filter(timeframe=timeframe)

        # return queryset
        return queryset


    # Serialize and Paginate the data    
    def retrieve(self, request, *args, **kwargs):
        # Get the queried data
        result = self.get_queryset()

        # Paginate the data
        result_page = self.paginate_queryset(result)
        
        # Serialize the data - (convert to JSON)
        serializer = SummaryStatSerializer(result_page, many=True)

        # Return the serialized and paginated data
        return self.get_paginated_response(serializer.data)