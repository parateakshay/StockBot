import numpy
from datetime import datetime
import yfinance as yf
import pandas as pd
import talib
import math
import time
import  csv
import winsound
from numpy import genfromtxt
import winsound
import backtrader as bt
import yagmail

yag = yagmail.SMTP("offline9967697690@gmail.com", 'KJSCE@Extc2020')



print("Playing the file 'Welcome.wav'")
wallet = 20;
profit_limit =0
holdings= 0
buying_price = 0
in_position = True
if holdings > 0:
    in_position = False
    wallet = wallet-holdings*buying_price

ticker = "ADA-USD";
filename = "data/temp.csv"



end = datetime.now()
data = yf.download(ticker, start="2021-05-1", end=end, period="ytd", interval="5m")
data.to_csv(filename)
print(data.head())



i = 4000

my_data = pd.read_csv(filename, delimiter=',', index_col=0)
close = my_data['Close'].to_numpy()
date = my_data.index.to_numpy()
print(type(close))


slow_moving_average = talib.SMA(close, timeperiod=30)
fast_moving_average = talib.SMA(close, timeperiod=7)

print(len(slow_moving_average))
print(len(fast_moving_average))

#
rsi = talib.RSI(close, timeperiod=13)

print('printing rsi first')
print(rsi)



macd, signal, hist = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
current_rsi = rsi[len(rsi)-i]
current_slow = signal[len(signal)-i]
current_fast = macd[len(macd)-i]

upper, middle, lower = talib.BBANDS(close, matype=0,timeperiod=30,nbdevup=2,nbdevdn=2)

print(len(lower))
print(len(upper))




while i>0:


    last_close = close[len(close)-i]

    # print("last close - {}".format(last_close))
    size = math.floor(wallet /last_close)
    # print("size = {}".format(size))
    if in_position:


        if (close[len(close)-i]<=lower[len(lower)-i] and rsi[len(rsi)-i]<35 and current_fast<=0) or rsi[len(rsi)-i]<25:
            #
            print("buying stock of {} at price {}------------------------------------------------------------ ".format(ticker,last_close))
            print("DATE : {}".format(date[len(date)-i]))
            # winsound.PlaySound('sounds/buying.wav', winsound.SND_FILENAME)
            holdings = size
            print("updated holding value {}".format(holdings))
            wallet = wallet - size*last_close
            print("updated wallet {}".format(wallet))
            in_position = False
            buying_price = last_close
            print("buying price = {}".format(buying_price))
            print("fast Moving average is {}".format(fast_moving_average[len(fast_moving_average)-i]))
            print("slow moving average is {}".format(slow_moving_average[len(slow_moving_average)-i]))
            print("rsi is {}".format(rsi[len(rsi)-i]))
            # yag.send("akshay.parate6@gmail.com", "stockbot - Buying {}".format(ticker), "buying stock of {} at price {} and updated wallet is {}".format(ticker,last_close,wallet))

            # time.sleep(2)
            i = i-1;

        else:
            # print("nothing to do chill  ")
            i = i - 1;

    if not in_position:

        if (close[len(close)-i]>=upper[len(upper)-i] and rsi[len(rsi)-i]>65 and current_fast>=0 and current_slow>=0) or rsi[len(rsi)-i]>80:
            selling_price = last_close
            if (selling_price-buying_price>=profit_limit):
                print("selling stocks of {} at price {}------------------------------------------------------------".format(ticker,last_close))
                print("DATE : {}".format(date[len(date) - i]))
                # winsound.PlaySound('sounds/selling.wav', winsound.SND_FILENAME)
                profit = holdings * last_close
                print("selling price of stock {}".format(profit))
                print("fast Moving average is {}".format(fast_moving_average[len(fast_moving_average) - i]))
                print("slow moving average is {}".format(slow_moving_average[len(slow_moving_average) - i]))
                print("rsi is {}".format(rsi[len(rsi) - i]))
                holdings = 0
                print("updated holding value {}".format(holdings))
                wallet = wallet+profit
                print("updated wallet {}".format(wallet))
                in_position = True

                # yag.send("akshay.parate6@gmail.com", "stockbot - Selling {}".format(ticker),"selling stock of {} at price {} and updated wallet is {}".format(ticker, last_close,wallet))

                # time.sleep(2)
                i = i-1;
            else:
                # print("nothing to do chill  ")
                i = i - 1;

        else:
            # print("nothing to do chill  ")
            i = i - 1;




print("wallet + profit = = = ".format(wallet))





