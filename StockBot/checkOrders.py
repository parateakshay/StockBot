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
client = Client(config.API_KEY, config.API_SECRET)


yag = yagmail.SMTP("offline9967697690@gmail.com", 'KJSCE@Extc2020')

def check_open_order(orderId,clientOrderId,symbol,selling_close,quantity):

   for i in range(0,5):
    orders = client.get_open_orders(symbol=symbol)
    if not orders:
        print("no open order")
        break
    else:
        winsound.PlaySound('sounds/alarm.wav', winsound.SND_FILENAME)
        break
        # result = client.cancel_order(
        #     symbol=symbol,
        #     orderId=orderId)
        # time.sleep(1)
        # try:
        #     print("sending order")
        #     order = client.create_order(
        #         symbol=symbol,
        #         side=SIDE_SELL,
        #         type=ORDER_TYPE_LIMIT,
        #         timeInForce=TIME_IN_FORCE_GTC,
        #         price=selling_close,
        #         # quantity of first coin for eg(in trxusdt it is trx)
        #         quantity=quantity)
        #     print(order)
        #     time.sleep(1)
        # except Exception as e:
        #     print("an exception occured - {}".format(e))
        #     winsound.PlaySound('sounds/alarm.wav', winsound.SND_FILENAME)

#
# orders = client.get_open_orders(symbol="SHIBUSDT")
# print(orders)