import pytz
from datetime import datetime
from typing import Literal
from dataclasses import dataclass
from urllib.parse import urlencode
import requests
from decouple import AutoConfig
from decimal import Decimal


config = AutoConfig(search_path="..")

ALPHA_VANTAGE_API_KEY = config("ALPHA_VANTAGE_API_KEY", default=None, cast = str)


def transform_alphavantage_result(timestamp_str, result):
    # unix_timestamp = result.get('t') / 1000.0
    # utc_timestamp = datetime.fromtimestamp(unix_timestamp, tz = pytz.timezone('UTC'))
    timestamp_format = '%Y-%m-%d %H:%M:%S' # dateutils
    eastern = pytz.timezone('US/Eastern')
    utc = pytz.utc
    utc_timestamp = eastern.localize(datetime.strptime(timestamp_str, timestamp_format)).astimezone(utc)
    return {
        'open_price' : Decimal(result['1. open']),
        'close_price' : Decimal(result['4. close']),
        'high_price' : Decimal(result['2. high']),
        'low_price' : Decimal(result['3. low']),
        'number_of_trades' : None,
        'volume' : int(result['5. volume']),
        'volume_weighted_average' : None,
        'raw_timestamp' : timestamp_str,
        'time' : utc_timestamp
    }

@dataclass
class AlphaVantageAPIClient:
    ticker : str = "AAPL"
    function: Literal["TIME_SERIES_INTRADAY", "TIME_SERIES_DAILY_ADJUSTED"] = "TIME_SERIES_INTRADAY"
    interval : Literal["1min", "5min", "15min", "30min", "60min"] = "1min"
    api_key : str = ""
    month : str = "2025-07"
    outputsize: Literal["compact", "full"] = "compact"  

    def get_api_key(self):
        return self.api_key or ALPHA_VANTAGE_API_KEY

        
    def get_params(self):
        params = {
            "function": self.function,
            "symbol": self.ticker,
            "apikey": self.get_api_key(),
        }
        if self.function == "TIME_SERIES_INTRADAY":
            params["interval"] = self.interval
        elif self.function == "TIME_SERIES_DAILY_ADJUSTED":
            params["outputsize"] = self.outputsize
        return params

    def get_headers(self):
        api_key = self.get_api_key()
        return {}
    
    def generate_url(self, pass_auth= False):
        path = "/query"
        url = f"https://www.alphavantage.co{path}"
        params = self.get_params()
        encoded_params = urlencode(params)
        url = f"{url}?{encoded_params}"
        if pass_auth:
            api_key = self.get_api_key()
            url += f"&apiKey={api_key}"
            
        return url

    def fetch_data(self):
        headers = self.get_headers()
        url = self.generate_url()
        response = requests.get(url, headers=headers)
        response.raise_for_status() # not 200/201
        print("AlphaVantage raw response:", response.json()) 
        return response.json()

    def get_stock_data(self):
        data = self.fetch_data()
            # Handle potential API error messages
        if not isinstance(data, dict):
            raise Exception(f"AlphaVantage returned non-dict response: {data}")

        if "Error Message" in data:
            raise Exception(f"AlphaVantage Error: {data['Error Message']}")

        if "Note" in data:
            raise Exception(f"AlphaVantage Rate Limit Hit: {data['Note']}")
        

        # dataset_key = [x for x in list(data.keys()) if not x.lower() == "meta data"][0]
        dataset_key = next((k for k in data.keys() if "Time Series" in k), None)
        if not dataset_key:
            raise Exception(f"No valid time series data found in response: {data}") 
        

        results = data[dataset_key]
        if not isinstance(results, dict):
            raise Exception(f"Expected dict for time series data, got {type(results)}")
        
        # dataset = []
        # for timestamp_str in results.keys():
        #     dataset.append(
        #         transform_alphavantage_result(timestamp_str, results.get(timestamp_str))
        #     )
        dataset = [
            transform_alphavantage_result(ts, results[ts])
            for ts in results
        ]
        return dataset
            
        
        