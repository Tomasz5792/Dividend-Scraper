# https://www.nasdaq.com/market-activity/stocks/oxlc
# Adding code to figuring out how to open data.

import pandas as pd
import requests
from bs4 import BeautifulSoup
import csv

# lists
tickers = []
stock_names = []
stock_prices = []
currencies = []
price_in_pounds = []

# Individual data
dollor_pound_rate = []
marketwatch_website = 'https://www.marketwatch.com/investing/fund/'


# opening previously saved table
def csv_to_list():
    global tickers
    global stock_names
    global stock_prices
    global currencies
    global dollor_pound_rate
    global price_in_pounds
    tickers = []
    stock_names = []
    stock_prices = []
    currencies = []
    dollor_pound_rate = []
    price_in_pounds = []

    table = open('Table.csv')
    csv_table = csv.reader(table)

    for i, row in enumerate(csv_table):
        if i == 0:
            continue
        tickers.append(row[2])
        stock_names.append(row[1])
        stock_prices.append(row[3])
        currencies.append(row[4])
        price_in_pounds.append(row[5])
        print('csv_to_list')


# Function to print table
def print_table(tickers, stock_names, stock_prices, currencies, price_in_pounds):
    table = pd.DataFrame(
        {
            'Stock Name': stock_names,
            'Ticker': tickers,
            'Stock Price': stock_prices,
            'Currency': currencies,
            'Stock Price (£)': price_in_pounds,
        })
    pd.set_option('max_colwidth', 10)
    print(table)
    # table.to_csv('Dividend Table.csv') #export to csv


# ---------------------------------
# information to get once
# ---------------------------------
def get_static_info(tickers, marketwatch_website):
    global stock_names
    stock_names = []
    global currencies
    currencies = []

    for ticker in tickers:
        ticker_page = f'{marketwatch_website}{ticker}'
        page = requests.get(ticker_page)

        soup = BeautifulSoup(page.content, 'html.parser')

        stock_name = soup.find(class_='company__name').get_text()

        data = soup.find(class_='intraday__price')
        currency = data.find(class_='character').get_text()

        stock_names.append(stock_name)
        currencies.append(currency)
        print('get_static_info')  # for testing only
    # print(stock_names) #for testing only
    # print(currencies) #for testing only


# ---------------------------------
# information to get multiple times
# ---------------------------------
def get_dollor_pound_rate():
    global dollor_pound_rate

    website = 'https://www.dollars2pounds.com/'
    page = requests.get(website)
    soup = BeautifulSoup(page.content, 'html.parser')
    dollor_pound_rate = soup.find(class_='fadable ratesValue').get_text()
    # print(dollor_pound_rate)#for testing only


# to get stock prices
def get_stock_price(tickers, marketwatch_website):
    global stock_prices
    stock_prices = []

    for ticker in tickers:
        ticker_page = f'{marketwatch_website}{ticker}'
        page = requests.get(ticker_page)

        soup = BeautifulSoup(page.content, 'html.parser')

        data = soup.find(class_='intraday__price')
        stock_price = data.find(class_='value').get_text()

        stock_price = stock_price.replace(',', '')  #

        stock_prices.append(stock_price)
        print('get_stock_price')  # for testing only
    # print(stock_prices) #for testing only


# to convert stock price to pounds
# doesn't parse only combines lists
def get_price_in_pounds(currencies, stock_prices):
    # print('get price in pound') #for testing only
    global price_in_pounds
    # print(price_in_pounds) #for testing only
    price_in_pounds = []
    # print(price_in_pounds) #for testing only

    for (currency, stock_price) in zip(currencies, stock_prices):
        if currency == '$':
            # print(f'{stock_price} {dollor_pound_rate}') #for testing only
            price_in_pound = float(stock_price) * float(dollor_pound_rate)
            # print(price_in_pound) #for testing only
        elif currency == 'p':
            price_in_pound = float(stock_price) / 100
            # print(price_in_pound) #for testing only
        else:
            price_in_pound = '*'
            # print(price_in_pound) #for testing only
        price_in_pounds.append(price_in_pound)
        print('get_price_in_pounds')  # for testing only
    # print(get_price_in_pounds) #for testing only


# main loop

csv_to_list()
print_table(tickers, stock_names, stock_prices, currencies, price_in_pounds)

while True:
    get_dollor_pound_rate()
    get_stock_price(tickers, marketwatch_website)
    get_price_in_pounds(currencies, stock_prices)
    print_table(tickers, stock_names, stock_prices, currencies, price_in_pounds)

    refresh = input('Enter r to refresh stock price: ')  # only stops loop


def print_lists(tickers, stock_names, stock_prices, currencies, price_in_pounds):
    print(tickers)
    print('')
    print(stock_names)
    print('')
    print(stock_prices)
    print('')
    print(currencies)
    print('')
    print(price_in_pounds)



