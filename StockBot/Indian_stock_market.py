import numpy
from datetime import datetime
import yfinance as yf
import pandas as pd
import talib
import math
import time
import winsound
filename = "data/temp.csv"
from numpy import genfromtxt
import yagmail

yag = yagmail.SMTP("offline9967697690@gmail.com", 'KJSCE@Extc2020')


quantity_first_crypto =5 #BIOCON
in_position_first = False
buying_price_first = 383

quantity_second_crypto=20 #HFCL
in_position_second = True
buying_price_second = 20

quantity_third_crypto = 4 #AIRTEL
in_position_third = True
buying_price_third = 10


quantity_fourth_crypto = 1 #TCS
in_position_fourth =False
buying_price_fourth = 3118


quantity_fifth_crypto =20  #zuari
in_position_fifth = True
buying_price_fifth = 10



winsound.PlaySound('sounds/jarvis.wav', winsound.SND_FILENAME)


def stock(ticker_x,ticker_y,quantity,in_position,buying_price):
    end = datetime.now()
    data = yf.download(ticker_x, start="2021-05-04", end=end, period="ytd", interval="5m")
    data.drop(data.tail(1).index, inplace=True)
    data.to_csv(filename)

    my_data = pd.read_csv(filename, delimiter=',', index_col=0)
    close = my_data['Close'].to_numpy()
    date = my_data.index.to_numpy()

    rsi = talib.RSI(close, timeperiod=13)
    macd, signal, hist = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
    current_rsi = rsi[len(rsi) - 1]
    current_slow = signal[len(signal) - 1]
    current_fast = macd[len(macd) - 1]

    upper, middle, lower = talib.BBANDS(close, matype=0, timeperiod=30, nbdevup=2, nbdevdn=2)

    last_close = close[len(close) - 1]
    if in_position:
        print("inside buying of {}".format(ticker_y))
        if (close[len(close) - 1] <= lower[len(lower) - 1] and rsi[len(rsi) - 1] < 30 and current_fast <= 0) or rsi[
            len(rsi) - 1] < 25:
            print("buying stock of {} at price {} ".format(ticker_y, last_close))
            winsound.PlaySound('sounds/buying.wav', winsound.SND_FILENAME)
            print("DATE : {}".format(date[len(date) - 1]))
            in_position = False
            buying_price = last_close
            contents = [
                "hiii this is your stockbot",
                "You have bought the stock of {}".format(ticker_y),
                "Price of buying is {}".format(last_close),
                "order id = {}".format(996769),
                "client order id = {}".format(7697690)
            ]
            subject = "STOCKBOT {}".format(ticker_y)

            yag.send("akshay.parate@somaiya.edu", subject, contents)

        else:
            print("nothing to do chill  ")
            time.sleep(10)

    else:
        print("nothing to do chill  ")
        time.sleep(10)

    if not in_position:
        print("inside selling of {}".format(ticker_y))
        if (close[len(close) - 1] >= upper[len(upper) - 1] and rsi[
            len(rsi) - 1] > 70 and current_fast >= 0 and current_slow >= 0) or rsi[len(rsi) - 1] > 80:
            selling_price = last_close
            if ((selling_price - buying_price)*quantity > 30):
                print("selling stocks of {} at price {}".format(ticker_y, last_close))
                winsound.PlaySound('sounds/selling.wav', winsound.SND_FILENAME)
                print("DATE : {}".format(date[len(date) - 1]))
                profit = quantity * selling_price - quantity * buying_price
                print("selling price of stock {}".format(profit))
                holdings = 0
                print("updated holding value {}".format(holdings))
                in_position = True
                profit_a = (buying_price - selling_price) * quantity * (-1)
                contents = [
                    "hiii this is your stockbot",
                    "You have sold the stock of {}".format(ticker_y),
                    "Price of selling is {}".format(last_close),
                    "profit is {}".format(profit_a),
                    "order id = {}".format(996769),
                    "client order id = {}".format(7697690)
                ]
                subject = "STOCKBOT {}".format(ticker_y)

                yag.send("akshay.parate@somaiya.edu", subject, contents)

            else:
                print("nothing to do chill  ")



        else:
            print("nothing to do chill  ")

    else:
        print()
    return in_position, buying_price


tickers = [['BIOCON.NS', 'BIOCON'],
          ['HFCL.NS', 'HFCL'],
          ['BHARTIARTL.NS', 'AIRTEL'],
          ['TCS.NS', 'TCS'],
          ['ZUARI.NS', 'zuari']]

dict = {'{}'.format(tickers[0][0]): [in_position_first,buying_price_first,quantity_first_crypto],
        '{}'.format(tickers[1][0]): [in_position_second,buying_price_second,quantity_second_crypto],
        '{}'.format(tickers[2][0]): [in_position_third,buying_price_third,quantity_third_crypto],
        '{}'.format(tickers[3][0]): [in_position_fourth,buying_price_fourth,quantity_fourth_crypto],
        '{}'.format(tickers[4][0]): [in_position_fifth,buying_price_fifth,quantity_fifth_crypto]}

while True:

    if (datetime.now().second == 0) and (datetime.now().minute % 5 == 0):
        print(dict)
        in_position_list = []
        buying_price_list = []
        i = 0
        for ticker in tickers:

            ticker_x = ticker[0]
            ticker_y = ticker[1]
            temp_position = dict['{}'.format(tickers[i][0])]
            in_position,buying_price = stock(ticker_x, ticker_y, temp_position[2], temp_position[0],temp_position[1])

            in_position_list.append(in_position)
            buying_price_list.append(buying_price)
            i = i+1

        print(in_position_list)
        in_position_first = in_position_list[0]
        in_position_second = in_position_list[1]
        in_position_third = in_position_list[2]
        in_position_fourth = in_position_list[3]
        in_position_fifth = in_position_list[4]
        print(buying_price_list)
        buying_price_first = buying_price_list[0]
        buying_price_second = buying_price_list[1]
        buying_price_third = buying_price_list[2]
        buying_price_fourth = buying_price_list[3]
        buying_price_fifth = buying_price_list[4]

        dict = {'{}'.format(tickers[0][0]): [in_position_first, buying_price_first, quantity_first_crypto],
                '{}'.format(tickers[1][0]): [in_position_second, buying_price_second, quantity_second_crypto],
                '{}'.format(tickers[2][0]): [in_position_third, buying_price_third, quantity_third_crypto],
                '{}'.format(tickers[3][0]): [in_position_fourth, buying_price_fourth, quantity_fourth_crypto],
                '{}'.format(tickers[4][0]): [in_position_fifth, buying_price_fifth, quantity_fifth_crypto]}

        time.sleep(10)
