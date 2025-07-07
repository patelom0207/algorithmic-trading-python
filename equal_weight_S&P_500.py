# Library Imports
import numpy as np
import pandas as pd
import requests
import xlsxwriter
import math

#Importing the S&P 500 stocks list
file_path = "C:/Users/patel_udh9l4n/OneDrive/algorithmic-trading-python/S&P_500_companies.csv"
stocks = pd.read_csv(file_path)

#Acquiring API Token
from .secrets import IEX_CLOUD_API_TOKEN

#Making first API call
symbol = "AAPL"
api_url = f'https://sandbox.iexapis.com/stock/{symbol}/quote/?tokan={IEX_CLOUD_API_TOKEN}'
data = requests.get(api_url).json()

#Parsing the data
data['latestPrice']
data['marketCap']

#Adding stocks data to pandas DataFrame
my_columns = ['Ticker', 'Price','Market Capitalization', 'Number Of Shares to Buy']
final_dataframe = pd.DataFrame(columns = my_columns)
final_dataframe = final_dataframe.append(pd.Series(['AAPL', data['latestPrice'], data['marketCap'], 'N/A'], index = my_columns), ignore_index = True)

#Looping through tickers in all S&P 500 stocks
final_dataframe = pd.DataFrame(columns = my_columns)
for symbol in stocks['Ticker']:
    api_url = f'https://sandbox.iexapis.com/stable/stock/{symbol}/quote?token={IEX_CLOUD_API_TOKEN}'
    data = requests.get(api_url).json()
    final_dataframe = final_dataframe.append(pd.Series([symbol, data['latestPrice'], data['marketCap'], 'N/A'], index = my_columns), ignore_index = True)
final_dataframe

# Function sourced from 
# https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

symbol_groups = list(chunks(stocks['Ticker'], 100))
symbol_strings = []
for i in range(0, len(symbol_groups)):
    symbol_strings.append(','.join(symbol_groups[i]))
#     print(symbol_strings[i])
final_dataframe = pd.DataFrame(columns = my_columns)

for symbol_string in symbol_strings:
#     print(symbol_strings)
    batch_api_call_url = f'https://sandbox.iexapis.com/stable/stock/market/batch/?types=quote&symbols={symbol_string}&token={IEX_CLOUD_API_TOKEN}'
    data = requests.get(batch_api_call_url).json()
    for symbol in symbol_string.split(','):
        final_dataframe = final_dataframe.append(pd.Series([symbol, data[symbol]['quote']['latestPrice'], data[symbol]['quote']['marketCap'], 'N/A'], index = my_columns), ignore_index = True)
    
final_dataframe

#Calculating number of shares to buy
portfolio_size = input("Enter the value of your portfolio:")

try:
    val = float(portfolio_size)
except ValueError:
    print("That's not a number! \n Try again:")
    portfolio_size = input("Enter the value of your portfolio:")

position_size = float(portfolio_size) / len(final_dataframe.index)
for i in range(0, len(final_dataframe['Ticker'])-1):
    final_dataframe.loc[i, 'Number Of Shares to Buy'] = math.floor(position_size / final_dataframe['Price'][i])
final_dataframe

#Initializing XLSX writer object
writer = pd.ExcelWriter('recommended_trades.xlsx', engine='xlsxwriter')
final_dataframe.to_excel(writer, sheet_name='Recommended Trades', index = False)