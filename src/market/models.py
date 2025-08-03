from django.db import models
from timescale.db.models.fields import TimescaleDateTimeField
from timescale.db.models.managers import TimescaleManager
from . import tasks

# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=120)
    ticker = models.CharField(max_length=20, unique = True, db_index = True)
    description = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    # sync_data = models.BooleanField(default=False)
    timestamp= models.DateTimeField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def save(self, *args, **kwargs):
        self.ticker = f"{self.ticker}".upper()
        # perform_sync = False
        # if self.sync_data:
        #     perform_sync = True
        #     self.sync_data = False
        super().save(*args, **kwargs)
        # if perform_sync:
        #     tasks.sync_company_stock_quotes.delay(self.pk)
        tasks.sync_company_stock_quotes.delay(self.pk)

class stockQuote(models.Model):
    """
    'open_price': 192.93,
    'close_price': 194.08,
    'high_price': 195.275,
    'low_price': 192.13,
    'number_of_trades': 382221,
    'volume': 31101847.0,
    'volume_weighted_average': 194.1131,
    'time': datetime.datetime(2025, 7, 25, 4, 0, tzinfo=<UTC>)
    """
    company = models.ForeignKey(
        Company,
        on_delete = models.CASCADE,
        related_name = "stock_quotes"
    )
    open_price = models.DecimalField(max_digits=10, decimal_places=4)
    close_price = models.DecimalField(max_digits=10, decimal_places=4)
    high_price = models.DecimalField(max_digits=10, decimal_places=4)
    low_price = models.DecimalField(max_digits=10, decimal_places=4)
    number_of_trades = models.BigIntegerField(blank=True, null=True)
    volume = models.BigIntegerField()
    volume_weighted_average = models.DecimalField(max_digits=10, decimal_places=4)
    time = TimescaleDateTimeField(interval="1 week")

    objects = models.Manager()
    timescale = TimescaleManager()

    class Meta:
        unique_together = [('company','time')]
