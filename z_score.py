#!/usr/bin/env python
# coding: utf-8

# In[6]:


import requests
import pandas as pd
import json

FMP_API_KEY = "bb423b45ad12e2fc041a86c3e3f9dce9"  # 

def get_symbol_mkt_cap(symbol):
    session = requests.Session()
    request = f"https://financialmodelingprep.com/api/v3/market-capitalization/{symbol}?apikey={FMP_API_KEY}".replace(" ", "")
    r = session.get(request)

    if r.status_code == requests.codes.ok:
        df = pd.DataFrame(json.loads(r.text))
        return df
    else:
        print(f"Failed to fetch market cap data for {symbol}. Response code: {r.status_code}")
        return None

def get_balance_sheet(symbol, lookback):
    session = requests.Session()
    request = f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{symbol}?period=quarter&limit={lookback}&apikey={FMP_API_KEY}".replace(" ", "")
    r = session.get(request)

    if r.status_code == requests.codes.ok:
        df = pd.DataFrame(json.loads(r.text))
        return df
    else:
        print(f"Failed to fetch balance sheet data for {symbol}. Response code: {r.status_code}")
        return None

def get_income_statement(symbol, lookback):
    session = requests.Session()
    request = f"https://financialmodelingprep.com/api/v3/income-statement/{symbol}?period=quarter&limit={lookback}&apikey={FMP_API_KEY}".replace(" ", "")
    r = session.get(request)

    if r.status_code == requests.codes.ok:
        df = pd.DataFrame(json.loads(r.text))
        return df
    else:
        print(f"Failed to fetch income statement data for {symbol}. Response code: {r.status_code}")
        return None

def get_key_metrics(symbol, lookback):
    session = requests.Session()
    request = f"https://financialmodelingprep.com/api/v3/key-metrics/{symbol}?period=quarter&limit={lookback}&apikey={FMP_API_KEY}".replace(" ", "")
    r = session.get(request)

    if r.status_code == requests.codes.ok:
        df = pd.DataFrame(json.loads(r.text))
        return df
    else:
        print(f"Failed to fetch key metrics data for {symbol}. Response code: {r.status_code}")
        return None

def calculate_altman_zscore(symbol, lookback):
    market_cap = get_symbol_mkt_cap(symbol=symbol)
    balance_sheet = get_balance_sheet(symbol=symbol, lookback=lookback)
    income_statement = get_income_statement(symbol=symbol, lookback=lookback)
    key_metrics = get_key_metrics(symbol=symbol, lookback=lookback)

    if market_cap is None or balance_sheet is None or income_statement is None or key_metrics is None:
        print("Unable to calculate the Altman Z-Score due to missing data.")
        return

    A = key_metrics["workingCapital"] / balance_sheet["totalAssets"]
    B = balance_sheet["retainedEarnings"] / balance_sheet["totalAssets"]
    C = (income_statement["ebitda"] - income_statement['depreciationAndAmortization']) / balance_sheet["totalAssets"]
    D = market_cap['marketCap'] / balance_sheet["totalLiabilities"]
    E = income_statement["revenue"] / balance_sheet["totalAssets"]

    altman_zscore = 1.2*A + 1.4*B + 3.3*C + 0.6*D + 1.0*E
    print(f"The Altman Z-Score for {symbol} is: {round(altman_zscore[0], 2)}")

def get_user_input():
    symbol = input("Enter the stock ticker: ")
    lookback = 1
    return symbol, lookback

def main():
    symbol, lookback = get_user_input()
    calculate_altman_zscore(symbol, lookback)

if __name__ == "__main__":
    main()


# In[ ]:





# In[ ]:




