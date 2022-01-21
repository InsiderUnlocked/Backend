# Purpose: Customizes admin table view

# Import Libraries
from django.contrib import admin
from .models import CongressPerson, CongressTrade, Ticker, SummaryStat

# Customize ticker admin view
class TickerAdmin(admin.ModelAdmin):
    # Fields that will appear in the admin table view
    list_display = ('ticker', 'company', 'marketcap', 'sector', 'industry',)
    # Field that we are searching for
    search_fields = ['ticker']

# Customize Congress Person admin view
class CongressPersonAdmin(admin.ModelAdmin):
    # Fields that will appear in the admin table view
    list_display = ('fullName', 'firstName', 'lastName', 'currentParty', 'currentChamber', 'currentState', 'totalTransactions',)
    # Field that we are searching for
    search_fields = ['fullName']

# Customize Congress Trade Admin
class CongressTradeAdmin(admin.ModelAdmin):
    # Fields that will appear in the admin table view
    list_display =  ('disclosureDate', 'name_fullName', 'transactionDate', 'owner', 'ticker', 'assetDescription', 'assetDetails', 'assetType', 'transactionType', 'amount', 'comment', 'name', 'pdf', 'ptrLink')
    # Column sorting for the dates
    list_filter = ('transactionDate',)
    # Field that we are searching for
    search_fields = ['name__fullName']

    def name_fullName(self, obj):
        return obj.name.fullName


# Customize Congress Trade Admin
class SummaryStatAdmin(admin.ModelAdmin):
    # Fields that will appear in the admin table view
    list_display =  ('total', 'purchases', 'sales', 'totalVolume', 'timeframe',)

# Register the admin views
admin.site.register(Ticker, TickerAdmin)
admin.site.register(CongressPerson, CongressPersonAdmin)
admin.site.register(CongressTrade, CongressTradeAdmin)
admin.site.register(SummaryStat, SummaryStatAdmin)