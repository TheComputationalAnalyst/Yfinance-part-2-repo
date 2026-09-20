import yfinance as yf
import pandas as pd
import numpy as np
from display import display_speedometer

stock = "AAPL"
ticker = yf.Ticker(stock)
close_price = yf.download(stock)['Close']
current_price = close_price.iloc[-1].item()

def obtain_price_targets(ticker):
    target = ticker.analyst_price_targets
    high_target = target['high']
    low_target = target['low']
    mean_target = target['mean']

    return high_target, low_target, mean_target


def obtain_calendar(ticker):
    calendar = ticker.calendar
    calendar = pd.DataFrame(calendar)
    dates = calendar.get("Earnings Date")  
    return calendar, dates

def obtain_financials(ticker):
    financials = ticker.financials
    return financials

def download_financials_to_txt(financials):
    with open("financials.txt", 'w') as financials_file:
        financials_file.write(financials.to_string())

def extract_financials(financials):
    total_revenue = financials.loc['Total Revenue']
    net_income = financials.loc['Net Income']
    return total_revenue, net_income

def obtain_insider_transactions(ticker):
    insider_transactions = ticker.insider_transactions
    return insider_transactions

def download_insider_transactions_to_txt(insider_transactions):
    with open("insider_transactions.txt", 'w') as transactions_file:
        transactions_file.write(insider_transactions.to_string())

def extract_insider_transactions(insider_transactions):
    transaction = insider_transactions.iloc[0]
    return transaction

high_target = obtain_price_targets(ticker)[0]
low_target = obtain_price_targets(ticker)[1]
mean_target = obtain_price_targets(ticker)[2]

calendar = obtain_calendar(ticker)[0]
dates = obtain_calendar(ticker)[1]

financials = obtain_financials(ticker)
download_financials_to_txt(financials)

total_revenue = extract_financials(financials)[0]
net_income = extract_financials(financials)[1]

insider_transactions = obtain_insider_transactions(ticker)
download_insider_transactions_to_txt(insider_transactions)
transaction = extract_insider_transactions(insider_transactions)

display_speedometer(high_target, low_target, mean_target, current_price)

