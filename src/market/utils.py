from django.apps import apps

def batch_insert_stock_data(dataset, company_obj=None, batch_size=1000,verbose=False):
    batch_size = 1000
    stockQuote = apps.get_model('market','stockQuote')
    if company_obj is None:
        raise Exception(f" Batch failed! Company object :{company_obj} invalid")
    for i in range(0, len(dataset), batch_size):    
        if verbose:
            print("doing chunk", i)
        batch_chunk = dataset[i:i+batch_size]
        chunked_quotes = []
        for data in batch_chunk:
            chunked_quotes.append(
                stockQuote(company=company_obj, **data)
            )
        stockQuote.objects.bulk_create(chunked_quotes, ignore_conflicts=True)
        if verbose:
            print("finished chunk", i)
    return len(dataset)