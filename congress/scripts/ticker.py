# @Author: Mohammed-Al Rasheed
# Purpose: Get financial data of stock from yahoo finance

# Import Libraries
import yfinance as yf


def getTickerData(ticker):
    # Get the data from yahoo fiannce 
    data = yf.Ticker(ticker)
    
    # get the sector, industry, company name, and market cap
    sector = data.info['sector']
    industry = data.info['industry']

    # if industry has '—', only get first part, as that is the industry which is the only thing we need
    if '—' in industry:
        industry = industry.split('—')[0]

    # get the company name
    company = data.info['longName']

    # get the market cap
    marketcap = data.info['marketCap']

    # determine if its a ETF
    quoteType = data.info['quoteType']
    
    # return the data
    return sector, industry, company, marketcap, quoteType

