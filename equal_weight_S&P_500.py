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