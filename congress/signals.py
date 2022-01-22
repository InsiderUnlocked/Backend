# @Author: Mohammed-Al Rasheed
# Purpose: Used in models.py to update the CongressPerson's tradesCount field 

# Update the stats of the summary stat object
def summaryStatUpdate(sender, instance, signal, *args, **kwargs):
    instance.updateStats()

# Update the stats of the ticker stat object
def tickerStatUpdate(sender, instance, signal, *args, **kwargs):
    instance.updateStats()

# Update the stats of the congress person stat object
def congressPersonStatUpdate(sender, instance, signal, *args, **kwargs):
    instance.updateStats()

