from django.contrib import admin

# Register your models here.
from .models import stockQuote, Company

admin.site.register(Company)

class stockQuoteAdmin(admin.ModelAdmin):
    list_display = ['company__ticker', 'close_price', 'time']
    list_filter = ['company__ticker', 'time']

    # for best practice
    # class Meta:
    #     model = stockQuote

admin.site.register(stockQuote, stockQuoteAdmin)