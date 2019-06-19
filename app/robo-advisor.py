import requests
import os
from dotenv import load_dotenv
import json
import pandas as pd 
import datetime

def to_usd(my_price):
    return "(${:,.2f})".format(my_price)

load_dotenv()

ALPHAVANTAGE_API_KEY = os.environ.get('ALPHAVANTAGE_API_KEY', 'Oh no you should fix the api key')

base_url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='
symbol = input('give me a ticker mofo ')
key = '&apikey=' + ALPHAVANTAGE_API_KEY

# request_url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&apikey=demo'

request_url = base_url + symbol + key


response = requests.get(request_url)
# print(type(response))
# print (response.status_code)
# print(response.text)

parsed_response = json.loads(response.text)
request_time = datetime.datetime.now().strftime("%b %d %Y %H:%M:%S")

tsd = parsed_response['Time Series (Daily)']
dates = list(tsd.keys())
latest_day = dates[0] # sort list so latest day is first assumes latest day is first...

last_refreshed = parsed_response['Meta Data']['3. Last Refreshed']
latest_close = tsd[latest_day]['4. close']

high_list = []
low_list = []
for date in dates:
    high_list.append(float(tsd[date]['2. high']))
    low_list.append(float(tsd[date]['3. low']))




highest_price = max(high_list)
lowest_price = min(low_list)


# breakpoint()

print("-------------------------")
print(f"SELECTED SYMBOL: {symbol}")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print(f"REQUEST AT: {request_time}")
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print(f"RECENT HIGH: {to_usd(float(highest_price))}")
print(f"RECENT LOW: {to_usd(float(lowest_price))}")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")


