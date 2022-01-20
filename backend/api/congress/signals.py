# Purpose: Used in models.py to update the CongressPerson's tradesCount field 

# Import Libraries
from django.db.models import signals
from django.dispatch import dispatcher

def tradesCount(sender, instance, signal, *args, **kwargs):
    # Import needs to be within function to access the CongressPerson table data
    from .models import CongressPerson
    
    # Runs through all the congress people and updates their 
    for person in CongressPerson.objects.all():
        person.tradesCount()

def summaryStatUpdate(sender, instance, signal, *args, **kwargs):
    instance.updateStats()

def tickerStatUpdate(sender, instance, signal, *args, **kwargs):
    instance.updateStats()

def congressPersonStatUpdate(sender, instance, signal, *args, **kwargs):
    instance.updateStats()

