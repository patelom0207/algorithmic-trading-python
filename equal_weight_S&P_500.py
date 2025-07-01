# Library Imports
import numpy as np
import pandas as pd
import requests
import xlsxwriter
import math

#Importing the S&P 500 stocks list
file_path = "C:\Users\patel_udh9l4n\Downloads\S&P 500 Companies (Standard and Poor 500) - basics.csv"
stocks = pd.read_csv(file_path)
