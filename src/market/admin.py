import zoneinfo
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.utils import timezone
from datetime import datetime
from rangefilter.filters import (
    DateTimeRangeFilterBuilder,
)

# Register your models here.
from .models import stockQuote, Company

admin.site.register(Company)

class stockQuoteAdmin(admin.ModelAdmin):
    list_display = ['company__ticker', 'close_price', 'localized_time','time']
    list_filter = [
        'company__ticker',
        ('time', DateTimeRangeFilterBuilder()),
        'time'
        ]
    readonly_fields = ['localized_time','time','raw_timestamp']

    # def display_raw_time(self, obj):
    #     data = float(obj.raw_timestamp)
    #     tz_name = "US/Eastern"
    #     user_tz = zoneinfo.ZoneInfo(tz_name)
    #     local_time = obj.time.astimezone(user_tz)
    #     unix_timestamp = data / 1000
    #     utc_timestamp = datetime.fromtimestamp(unix_timestamp, tz=user_tz)
    #     return local_time.strftime("%b %d, %Y, %I:%M %p (%Z)")
    
    def localized_time(self, obj):
        tz_name = "US/Eastern"
        user_tz = zoneinfo.ZoneInfo(tz_name)
        local_time = obj.time.astimezone(user_tz)
        return local_time.strftime("%b %d, %Y, %I:%M %p (%Z)")
    
    def get_queryset(self, request):
        tz_name = "US/Eastern"
        user_tz = zoneinfo.ZoneInfo(tz_name)
        timezone.activate(user_tz)
        return super().get_queryset(request)
    
    # for best practice
    # class Meta:
    #     model = stockQuote

admin.site.register(stockQuote, stockQuoteAdmin)