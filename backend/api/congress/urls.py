# Purpose: Registering all the endpoints

# Import Libraries
from django.urls import include, path
from rest_framework import routers
from . import views

# Create a router and register our viewsets with it.
router = routers.DefaultRouter()

# Returns all of the Congress Transactions
router.register(r'congress-trades', views.AllCongressViewSet, basename='congressAll')

# Returns all of the Congress People who have made a transaction
router.register(r'congress-all', views.AllCongressPeopleViewSet, basename='congressPersonAll')

# Returns all the transactions of a certain stock ticker 
router.register(r'ticker', views.TickerViewSet, basename='Ticker')

# Returns all the transactions of a specific congress person 
router.register(r'congress-person', views.CongressPersonViewSet, basename='congressPerson')

# Returns the summary stats for congeress-trades endpoint 
router.register(r'summary-stats', views.SummaryStatsViewSet, basename='summaryStats')

# Returns the summary stats for Ticker endpoint 
router.register(r'ticker-stats', views.TickerStatsViewSet, basename='tickerStats')

# Returns the summary stats for Ticker endpoint 
router.register(r'congress-stats', views.CongressStatsViewSet, basename='congressStats')


# Wire up our API using automatic URL routing.
urlpatterns = [
    path('government/', include(router.urls)),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]