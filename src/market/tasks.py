from django.apps import apps
from .utils import batch_insert_stock_data
import helpers.clients as helper_clients
from django.utils import timezone
from datetime import timedelta
from celery import shared_task
import time

@shared_task
def sync_company_stock_quotes(company_id,days_ago=32,dateformat="%Y-%m-%d", verbose=False):
    Company = apps.get_model("market", "Company")
    try:
        company_obj = Company.objects.get(id=company_id)
    except:
        company_obj = None
    if company_obj is None:
        raise Exception(f"{company_obj} invalid")
    company_ticker = company_obj.ticker
    if company_ticker is None:
        raise Exception(f"{company_ticker} invalid")
    
    now = timezone.now()
    start_date = now - timedelta(days=days_ago)

    to_date = start_date + timedelta(days=days_ago+1)
    to_date = to_date.strftime(dateformat)
    from_date = start_date.strftime(dateformat)

    client = helper_clients.PologyonAPIClient(
        ticker=company_ticker,
        from_date=from_date,
        to_date=to_date
    )
    dataset = client.get_stock_data()
    if verbose:
        print(f"Length of the dataset : {len(dataset)}")
    
    batch_insert_stock_data(dataset=dataset, company_obj=company_obj, verbose=verbose)
    

@shared_task
def sync_stocks_data(days_ago=2):
    Company = apps.get_model("market", "Company")
    companies = Company.objects.filter(active=True).values_list('id',flat=True)
    for company_id in companies:
        # managed by celery
        sync_company_stock_quotes.delay(company_id=company_id,days_ago=days_ago)
    

@shared_task
def sync_historical_stock_data(years_ago=1, company_ids = []):
    Company = apps.get_model("market", "Company")
    qs = Company.objects.filter(active=True)
    if len(company_ids) > 0:
        qs = qs.filter(id__in=company_ids)
    companies = qs.values_list('id',flat=True)
    for company_id in companies:
        days_starting_ago = 20*12*years_ago
        batch_size = 30
        for i in range(30, days_starting_ago, batch_size):
            sync_company_stock_quotes.delay(company_id=company_id,days_ago=i)
            time.sleep(1.5)