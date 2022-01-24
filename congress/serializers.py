# @Author: Farhan Rehman
# Purpose: Converts SQLite queries response to JSON

# Imports
from rest_framework.serializers import ModelSerializer, ReadOnlyField
from rest_framework import serializers

from .models import CongressTrade, CongressPerson, Ticker, SummaryStat

# Abstraction is integrated due to django within all of these classes
class TickerSerializer(serializers.ModelSerializer):
    class Meta:
        # Database table
        model = Ticker
        # Fields to appear on the response
        fields = ('ticker', 'company', 'marketcap', 'sector', 'industry', 'totalTransactions', 'totalVolumeTransactions', 'purchases', 'sales',)

class CongressPersonSerializer(serializers.ModelSerializer):
    class Meta:
        # Database table
        model = CongressPerson
        # Fields to appear on the response
        fields = ('fullName', 'currentParty', 'currentChamber',  'currentState', 'image', 'totalTransactions', 'totalVolumeTransactions', 'purchases', 'sales',)

class CongressTradeSerializer(serializers.ModelSerializer):
    # Gets ForignKey field to appear on the response, refer to ERD Diagram to get a better understanding of the connection between the models
    name = ReadOnlyField(source='name.fullName')
    ticker = ReadOnlyField(source='ticker.ticker')

    # firstName = ReadOnlyField(source='name.firstName')
    # lastName = ReadOnlyField(source='name.lastName')
    # bioguide = ReadOnlyField(source='name.bioguide')

    class Meta:
        # Database table
        model = CongressTrade
        # Fields to appear on the response
        # fields = ('name', 'bioguide','firstName','lastName', 'ticker', 'transactionDate', 'assetType', 'transactionType', 'amount',  'ptrLink')
        fields = ('name', 'ticker', 'transactionDate', 'assetType', 'transactionType', 'amount',  'ptrLink')

class SummaryStatSerializer(serializers.ModelSerializer):
    class Meta:
        # Database table
        model = SummaryStat
        # Fields to appear on the response
        # __all__ includes all fields in the model in the response
        fields = "__all__"
