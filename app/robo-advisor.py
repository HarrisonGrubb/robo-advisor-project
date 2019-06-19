import requests
import os
from dotenv import load_dotenv
import json
import pandas as pd 

load_dotenv()

ALPHAVANTAGE_API_KEY = os.environ.get('ALPHAVANTAGE_API_KEY', 'Oh no you should fix the api key')

base_url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='
symbol = input('give me a ticker mofo ')
key = '&apikey=' + ALPHAVANTAGE_API_KEY

# request_url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&apikey=demo'

request_url = base_url + symbol + key


response = requests.get(request_url)
print(type(response))
print (response.status_code)
print(response.text)

parsed_response = json.loads(response.text)

quit()

print("-------------------------")
print("SELECTED SYMBOL: XYZ")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: 2018-02-20 02:00pm")
print("-------------------------")
print("LATEST DAY: 2018-02-20")
print("LATEST CLOSE: $100,000.00")
print("RECENT HIGH: $101,000.00")
print("RECENT LOW: $99,000.00")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")


