import time
from datetime import datetime
import pandas as pd
import websocket, json, pprint, talib, numpy
import config
from binance.client import Client
from datetime import datetime
import talib
import math
import time
import winsound
import  csv
from binance.enums import *
client = Client(config.API_KEY, config.API_SECRET,{"verify": True, "timeout": 20})


tickers = ['XLMUSDT','DOGEUSDT','XRPUSDT','ADAUSDT','TRXUSDT','VETUSDT','DOCKUSDT','IOSTUSDT']

result = []

for ticker in tickers:

    wallet = 25;
    holdings= 0
    buying_price = 0
    in_position = True
    # if holdings > 0:
    #     in_position = False
    #     wallet = wallet-holdings*buying_price
    no_of_trades = 0

    bars = client.get_historical_klines(interval=Client.KLINE_INTERVAL_5MINUTE,symbol=ticker,start_str="01 May 2021",end_str="15 May 2021")
    for line in bars:
        del line[5:]
    data = pd.DataFrame(bars, columns=['date', 'open', 'high', 'low', 'Close'], dtype=numpy.float64)
    # data.to_csv("temp.csv")
    # print(data.head())
    close = data['Close'].to_numpy()
    date = data['date'].to_numpy()
    rsi = talib.RSI(close, timeperiod=13)

    i = 4000

    macd, signal, hist = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
    current_rsi = rsi[len(rsi)-i]
    current_slow = signal[len(signal)-i]
    current_fast = macd[len(macd)-i]

    upper, middle, lower = talib.BBANDS(close, matype=0,timeperiod=30,nbdevup=2,nbdevdn=2)

    # print(len(lower))
    # print(len(upper))
    # print(len(rsi))
    # print("yes")

    buy_hint = False
    sell_hint = False
    temp = []




    while i>0:


        last_close = close[len(close)-i]

        # print("last close - {}".format(last_close))
        size = math.floor(wallet /last_close)

        # print("size = {}".format(size))
        if in_position:


            if ((close[len(close)-i]<=lower[len(lower)-i]  and rsi[len(rsi)-i]<30 and macd[len(macd)-i]<=0) or rsi[len(rsi)-i]<15):
            #     buy_hint = True
            #
            #
            # if(buy_hint and rsi[len(rsi)-i]>30):
            #     buy_hint = False

                # print("buying stock of {} at price {}------------------------------------------------------------ ".format(ticker,last_close))

                timestamp = date[len(date)-i] / 1000
                dt_object = datetime.fromtimestamp(timestamp)
                # print("DATE : {}".format(dt_object))
                # winsound.PlaySound('sounds/buying.wav', winsound.SND_FILENAME)
                holdings = size
                # print("updated holding value {}".format(holdings))
                wallet = wallet - size*last_close
                # print("updated wallet {}".format(wallet))
                in_position = False
                buying_price = last_close
                # print("buying price = {}".format(buying_price))
                profit_limit = last_close * 0.03
                # print("rsi is {}".format(rsi[len(rsi)-i]))
                # print("bollinger band {}".format(lower[len(lower)-i]))
                # print("close {}".format(last_close))
                # yag.send("akshay.parate6@gmail.com", "stockbot - Buying {}".format(ticker), "buying stock of {} at price {} and updated wallet is {}".format(ticker,last_close,wallet))

                # time.sleep(2)
                i = i-1;

            else:
                # print("nothing to do chill  ")
                i = i - 1;

        if not in_position:

            if ((close[len(close)-i]>=upper[len(upper)-i] and rsi[len(rsi)-i]>70 and macd[len(macd)-i]>=0) or rsi[len(rsi)-i]<15):
            #     sell_hint = True
            #
            # if(sell_hint and rsi[len(rsi)-i]<70):
            #     sell_hint = False
                selling_price = last_close
                if (selling_price>buying_price and selling_price>buying_price+profit_limit):

                    # print("selling stocks of {} at price {}------------------------------------------------------------".format(ticker,last_close))
                    timestamp = date[len(date) - i] / 1000
                    dt_object = datetime.fromtimestamp(timestamp)
                    # print("DATE : {}".format(dt_object))
                    # winsound.PlaySound('sounds/selling.wav', winsound.SND_FILENAME)
                    profit = holdings * last_close
                    # print("selling price of stock {}".format(profit))

                    # print("rsi is {}".format(rsi[len(rsi) - i]))
                    holdings = 0
                    # print("updated holding value {}".format(holdings))
                    wallet = wallet+profit
                    # print("updated wallet {}".format(wallet))
                    temp.append(wallet)
                    in_position = True
                    no_of_trades = no_of_trades+1
                    # yag.send("akshay.parate6@gmail.com", "stockbot - Selling {}".format(ticker),"selling stock of {} at price {} and updated wallet is {}".format(ticker, last_close,wallet))

                    # time.sleep(2)
                    i = i-1;
                else:
                    # print("nothing to do chill  ")
                    sell_hint = False
                    i = i - 1;

            else:
                # print("nothing to do chill  ")
                i = i - 1;
    if(no_of_trades>0):
        print(ticker)
        print("no of trades = {}".format(no_of_trades))
        print(temp[-1])
    else:
        print(ticker)
        print("no of trades = {}".format(no_of_trades))
