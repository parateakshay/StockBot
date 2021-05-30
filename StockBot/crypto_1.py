import time
from datetime import datetime
import pandas as pd
import websocket, json, pprint, talib, numpy
import config
from binance.client import Client
import talib
import math
import time
import yagmail
import winsound
import backtrader as bt
import  csv
from binance.enums import *
from checkOrders import check_open_order
client = Client(config.API_KEY, config.API_SECRET,{"verify": True, "timeout": 20})
yag = yagmail.SMTP("offline9967697690@gmail.com", 'KJSCE@Extc2020')
winsound.PlaySound('sounds/jarvis.wav', winsound.SND_FILENAME)

quantity_first_crypto =135 #VET
in_position_first = False
buying_price_first = 0.1296

quantity_second_crypto=35 #XLM
in_position_second = False
buying_price_second = 0.43113

quantity_third_crypto = 55 #HBAR
in_position_third = False
buying_price_third =0.25344


quantity_fourth_crypto = 211 #IOST
in_position_fourth =False
buying_price_fourth = 0.0517


quantity_fifth_crypto =40  #DOGE
in_position_fifth = False
buying_price_fifth = 0.3477

def new_crypto(ticker_x,ticker_y,quantity,in_position,buying_price):

    first_asset_fees = quantity_first_crypto * 0.001 * buying_price
    selling_quantity = quantity - quantity * 0.002
    ticker = ticker_y
    bars = client.get_historical_klines(ticker_x, Client.KLINE_INTERVAL_5MINUTE, "19 May 2021")
    for line in bars:
        del line[5:]
    data = pd.DataFrame(bars, columns=['date', 'open', 'high', 'low', 'close'], dtype=numpy.float64)
    data.set_index('date', inplace=True)
    xyz = data.tail(1)
    selling_close = xyz['close'].to_numpy()
    data.drop(data.tail(1).index, inplace=True)
    # data.to_csv(filename)
    close = data['close'].to_numpy()

    date = data.index.to_numpy()

    # slow_moving_average = talib.SMA(close, timeperiod=30)
    # fast_moving_average = talib.SMA(close, timeperiod=7)
    rsi = talib.RSI(close, timeperiod=13)

    # print('printing rsi first')
    # print(rsi)
    macd, signal, hist = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
    current_rsi = rsi[len(rsi) - 1]
    current_slow = signal[len(signal) - 1]
    current_fast = macd[len(macd) - 1]

    upper, middle, lower = talib.BBANDS(close, matype=0, timeperiod=30, nbdevup=2, nbdevdn=2)
    # print(rsi)

    # macd, signal, hist = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)

    last_close = close[len(close) - 1]
    print("last close - {}".format(last_close))
    # print("holdings = {}".format(holdings))

    if in_position:
        print("inside buying of {}".format(ticker_y))

        if (close[len(close) - 1] <= lower[len(lower) - 1] and rsi[len(rsi) - 1] < 30 and current_fast <= 0) or rsi[
            len(rsi) - 1] < 25:
            print("buying stock of {} at price {} ".format(ticker, last_close))
            winsound.PlaySound('sounds/buying.wav', winsound.SND_FILENAME)
            print("DATE : {}".format(date[len(date) - 1]))
            first_asset_fees = quantity * 0.001 * last_close

            try:
                print("sending order")
                order = client.create_order(
                    symbol=ticker_x,
                    side=SIDE_BUY,
                    type=ORDER_TYPE_LIMIT,
                    timeInForce=TIME_IN_FORCE_GTC,
                    price=selling_close[0],
                    quantity=quantity)
                print(order)
                orderId = order['orderId']
                clientOrderId = order['clientOrderId']
                symbol = order['symbol']
                contents = [
                    "hiii this is your stockbot",
                    "You have bought the stock of {}".format(ticker),
                    "Price of buying is {}".format(last_close),
                    "order id = {}".format(orderId),
                    "client order id = {}".format(clientOrderId)
                ]
                check_open_order(orderId,clientOrderId,symbol,selling_close[0],quantity)

                subject = "STOCKBOT {}".format(ticker)

                yag.send("akshay.parate@somaiya.edu", subject, contents)
                yag.send("gargr9198@gmail.com", subject, contents)


            except Exception as e:
                print("an exception occured - {}".format(e))
                winsound.PlaySound('sounds/alarm.wav', winsound.SND_FILENAME)


            yag.send("akshay.parate6@gmail.com", "checking", "buy {}".format(ticker))

            in_position = False
            buying_price = last_close
            print("in position = {}".format(in_position))

        else:
            print("nothing to do chill  ")

    if not in_position:
        print("inside selling of {}".format(ticker))

        if (close[len(close) - 1] >= upper[len(upper) - 1] and rsi[
            len(rsi) - 1] > 70 and current_fast >= 0 and current_slow >= 0) or rsi[len(rsi) - 1] > 80:
            selling_price = last_close
            second_asset_fees = last_close * quantity * 0.001
            profit_limit = buying_price + buying_price * 0.05
            if (selling_price>buying_price and selling_price>=profit_limit):
                print("selling stocks of {} at price {}".format(ticker, last_close))
                winsound.PlaySound('sounds/selling.wav', winsound.SND_FILENAME)
                print("DATE : {}".format(date[len(date) - 1]))
                try:
                    print("sending order")
                    order = client.create_order(
                        symbol=ticker_x,
                        side=SIDE_SELL,
                        type=ORDER_TYPE_LIMIT,
                        timeInForce=TIME_IN_FORCE_GTC,
                        price=selling_close[0],
                        # quantity of first coin for eg(in trxusdt it is trx)
                        quantity=quantity)
                    print(order)
                    orderId = order['orderId']
                    clientOrderId = order['clientOrderId']
                    symbol = order['symbol']
                    check_open_order(orderId, clientOrderId, symbol, selling_close[0], selling_quantity)
                    profit_a = (buying_price - selling_price) * quantity * 78 * (-1)
                    contents = [
                        "hiii this is your stockbot",
                        "You have sold the stock of {}".format(ticker),
                        "Price of selling is {}".format(last_close),
                        "profit is {}".format(profit_a),
                        "order id = {}".format(orderId),
                        "client order id = {}".format(clientOrderId)
                    ]

                    subject = "STOCKBOT {}".format(ticker)

                    yag.send("akshay.parate@somaiya.edu", subject, contents)
                    yag.send("gargr9198@gmail.com", subject, contents)

                except Exception as e:
                    print("an exception occured - {}".format(e))
                    winsound.PlaySound('sounds/alarm.wav', winsound.SND_FILENAME)
                yag.send("akshay.parate6@gmail.com", "checking", "sell {}".format(ticker))
                in_position = True

                print("in position = {}".format(in_position))
            else:
                print("nothing to do chill  ")


        else:
            print("nothing to do chill  ")

    else:
        print()
    return in_position,buying_price



tickers = [['VETUSDT', 'VET'],
          ['XLMUSDT', 'XLM'],
          ['HBARUSDT', 'HBAR'],
          ['IOSTUSDT', 'IOST'],
          ['DOGEUSDT', 'DOGE']]

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
            in_position,buying_price = new_crypto(ticker_x, ticker_y, temp_position[2], temp_position[0],temp_position[1])

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

        # df.to_csv("new.csv")











