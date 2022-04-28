import alpaca_trade_api as tradeapi
import time
import json
import requests
################# Setting up Alpaca ###################
# API Info for fetching data, portfolio, etc. from Alpaca
BASE_URL = "https://paper-api.alpaca.markets"
ALPACA_API_KEY = "PK8TTRRC3ZH69CJTXW5W"
ALPACA_SECRET_KEY = "3PUzbRdCn3vwqDe0TGg79RFFF7H75rwK9011UU6F"

# Instantiate REST API Connection
api = tradeapi.REST(key_id=ALPACA_API_KEY,
                    secret_key=ALPACA_SECRET_KEY,
                    base_url=BASE_URL,
                    api_version='v2')

# Fetch Account
account = api.get_account()

# Print Account Details
print(account.id, account.equity, account.status)

#######################################################
############ Manual Buy or Sell #######################
#######################################################
print('Hello welcome to you Alpaca account. You currently have: ')

# Get a list of all of our positions.
portfolio = api.list_positions()

# Print the quantity of shares for each position.
for position in portfolio:
    print("{} shares of {}".format(position.qty, position.symbol))
########################################################

order1 = input("Do you want to buy or sell something: ")

if order1 == 'yes':
    symName = input("What do you want to sell/buy: ")
    buyOrSell = input("Do you want to sell or buy: ")

    api.submit_order(symbol=symName,
                     qty=1,
                     side=buyOrSell,
                     type='market',
                     time_in_force='day')
    dictionary = {
        "Stock": symName,
        "Buy/Sell": buyOrSell,
    }

    with open("sample.json", "w") as outfile:
        json.dump(dictionary, outfile)

###########################################################
# Going to use yahoo finance to get information on AAPL ##
###########################################################
myKey = "3eivhlXEY68HheNJtvShg6PlVNRA3r5C8A7wiQoF"

url = "https://yfapi.net/v6/finance/quote"
querystring = {"symbols": "AAPL"}

headers = {'x-api-key': myKey}

response = requests.request("GET", url, headers=headers, params=querystring)

#########################################################
############# Automatic Trading #########################
#########################################################
while(True):
  # Get a list of all of our positions.
  portfolio = api.list_positions()

  if position.symbol == 'AAPL':  # You have an Apple stock to trade
    aapl_position = api.get_position('AAPL')
    if float(aapl_position.unrealized_pl
             ) > 100:  # if you have made more than $100
        api.submit_order(symbol='AAPL',
                         qty=1,
                         side='sell',
                         type='market',
                         time_in_force='day')
        dictionary = {"Stock": "AAPL", "Buy/Sell": "Sell"}
        with open("sample.json", "w") as outfile:
            json.dump(dictionary, outfile)

    if float(aapl_position.unrealized_pl
             ) < -100:  # if you have lost most than $100
        api.submit_order(symbol='AAPL',
                         qty=1,
                         side='sell',
                         type='market',
                         time_in_force='day')

        dictionary = {"Stock": "AAPL", "Buy/Sell": "Sell"}
        with open("sample.json", "w") as outfile:
            json.dump(dictionary, outfile)

  else:  # You do not have an Apple stock so may buy one?
    stock_json = response.json()
    trailingPE = stock_json['quoteResponse']['result'][0]['trailingPE']
    forwardPE = stock_json['quoteResponse']['result'][0]['forwardPE']

    if trailingPE < 50 or forwardPE < 50:
        api.submit_order(symbol='AAPL',
                         qty=1,
                         side='buy',
                         type='market',
                         time_in_force='day')
        dictionary = {"Stock": "AAPL", "Buy/Sell": "Sell"}
        with open("sample.json", "w") as outfile:
            json.dump(dictionary, outfile)
  time.sleep(300)