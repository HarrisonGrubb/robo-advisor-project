import requests
import os
from dotenv import load_dotenv
import json
import csv 
import pandas as pd 
import datetime
import matplotlib.pyplot as plt

def to_usd(my_price):
    return "(${:,.2f})".format(my_price)

load_dotenv()

ALPHAVANTAGE_API_KEY = os.environ.get('ALPHAVANTAGE_API_KEY', 'Oh no you should fix the api key')

base_url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='
key = '&apikey=' + ALPHAVANTAGE_API_KEY

flag = False

while flag == False:
    symbol = input('Please input a stock symbol ')
    if symbol.isdigit() == True:
        print('No numbers please')
    elif len(symbol) > 5: # 5 so you could also look up etfs and other traded funds :)
        print ('That is a little too long for a ticker')
    else:
        request_url = base_url + symbol + key
        response = requests.get(request_url)
        if response.status_code == 200:
            symbol = symbol.upper()
            flag = True
        else:
            print("Something isn't quite right can you pick another symbol?")


parsed_response = json.loads(response.text)
request_time = datetime.datetime.now().strftime("%b %d %Y %H:%M:%S")

try:
    parsed_response['Time Series (Daily)']
except:
    print('Oh no, something is wrong. Can we start over?')
    print('Shutting program down...')
    exit()

tsd = parsed_response['Time Series (Daily)']
dates = list(tsd.keys())
latest_day = dates[0] 

last_refreshed = parsed_response['Meta Data']['3. Last Refreshed']
latest_close = tsd[latest_day]['4. close']
latest_open = tsd[latest_day]['1. open']
latest_volume = tsd[latest_day]['5. volume']

high_list = []
low_list = []
if len(dates) > 100:
    for date in range(0,100):
        high_list.append(float(tsd[date]['2. high']))
else:
    for date in dates:
        high_list.append(float(tsd[date]['2. high']))

for date in dates:
    # high_list.append(float(tsd[date]['2. high']))
    low_list.append(float(tsd[date]['3. low']))

highest_price = max(high_list)
lowest_price = min(low_list)

### recommendation
# change sp500 and stock 
# get sp500 for comparison
spy_url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=SPY' + key
spy_request = requests.get(spy_url)
spy_response = json.loads(spy_request.text)
spy_tsd = spy_response['Time Series (Daily)']

#calculate the growth/decline of spy 
spy_today = float(spy_tsd[dates[0]]['4. close']) 
spy_yesterday = float(spy_tsd[dates[1]]['4. close'])
spy_change = (spy_today - spy_yesterday)/spy_yesterday

#daily change of selected stock
user_choice_today = float(tsd[dates[0]]['4. close'])
user_choice_yesterday = float(tsd[dates[1]]['4. close'])
user_choice_change = (user_choice_today - user_choice_yesterday) / user_choice_yesterday 
#compare spy to change in selected stock and 
# if change in sp500 is > than change in selected stock sell if greater buy


if spy_change > user_choice_change:
    recommendation = 'Sell'
    reason = 'did worse than the market'
else:
    recommendation = 'Buy'
    reason = 'did better than the market'

wkly_adj = 'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol='
wkly_request_url = wkly_adj + symbol + key
wk_response = requests.get(wkly_request_url)
parsed_wk = json.loads(wk_response.text)

wkly_ts = parsed_wk["Weekly Time Series"]
wk_dates = list(wkly_ts.keys())

wk_high_list = []
wk_low_list = []

if len(wk_dates) < 52:
    for date in wk_dates:
        wk_high_list.append(float(wkly_ts[date]['2. high']))
        wk_low_list.append(float(wkly_ts[date]['3. low']))
else:
    for date in range(0, 53):
        wk_high_list.append(float(wkly_ts[wk_dates[date]]['2. high']))
        wk_low_list.append(float(wkly_ts[wk_dates[date]]['3. low']))





week52_high = max(wk_high_list)
week52_low = min(wk_low_list)

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
print(f"52 WEEK HIGH: {to_usd(float(week52_high))}")
print(f"52 WEEK LOW: {to_usd(float(week52_low))}")
print("-------------------------")
print(f"RECOMMENDATION: {recommendation}")
print(f"RECOMMENDATION REASON: {symbol} {reason}")
print("-------------------------")
print('WRTING TO CSV!')
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")

csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", f'{symbol}.data.csv')

with open(csv_file_path, "w") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames = ['stock_symbol', 'time_stamp', 'open', 'recent_high', 'recent_low', 'close', 'volume'])
    writer.writeheader()
    for date in dates:
        writer.writerow({
            'stock_symbol' : symbol,
            'time_stamp': date, 
            'open' : tsd[date]['1. open'], 
            'recent_high' : tsd[date]['2. high'], 
            'recent_low': tsd[date]['3. low'], 
            'close' : tsd[date]['4. close'], 
            'volume': tsd[date]['5. volume']})


####visuals
chart_data = pd.DataFrame.from_dict(wkly_ts)
two_col_df = chart_data.drop(['1. open', '4. close', '5. volume']).T
two_col_df['2. high'] = pd.to_numeric(two_col_df['2. high'])
two_col_df['3. low'] = pd.to_numeric(two_col_df['3. low'])

two_col_df = two_col_df.iloc[::-1]
# it was helpful earlier to have in reverse chron order, now we need to undo that otherwise our charts are backwards :)

plt.plot(two_col_df['2. high'], label = '52 week high')
plt.plot(two_col_df['3. low'], label = '52 week low')
plt.legend(loc = 'upper left')
plt.show(block = False)
input('Press <ENTER> to stop the program')


# help
# re-ordering df 
#https://stackoverflow.com/questions/20444087/right-way-to-reverse-pandas-dataframe
#https://stackoverflow.com/questions/19125722/adding-a-legend-to-pyplot-in-matplotlib-in-the-most-simple-manner-possible