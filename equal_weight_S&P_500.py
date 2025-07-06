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