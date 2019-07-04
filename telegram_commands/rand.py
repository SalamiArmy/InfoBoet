# coding=utf-8
import json
import urllib


def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    bot.sendMessage(chat_id=chat_id, text=get_exchange_data())
    return True

def get_exchange_data():
    usdurl = 'https://api.exchangeratesapi.io/latest?base=USD'
    gbpurl = 'https://api.exchangeratesapi.io/latest?base=GBP'
    eururl = 'https://api.exchangeratesapi.io/latest?base=EUR'
    audurl = 'https://api.exchangeratesapi.io/latest?base=AUD'
    data1 = json.load(urllib.urlopen(usdurl))
    data2 = json.load(urllib.urlopen(gbpurl))
    data3 = json.load(urllib.urlopen(eururl))
    data4 = json.load(urllib.urlopen(audurl))
    zarusd = float(data1['rates']['ZAR'])
    zargbp = float(data2['rates']['ZAR'])
    zareur = float(data3['rates']['ZAR'])
    zaraud = float(data4['rates']['ZAR'])
    formatted_exchange_data = '1 USD = ' + str(zarusd) + ' ZAR\n1 GBP = ' + str(zargbp) + ' ZAR\n1 EUR = ' + str(zareur) + ' ZAR\n1 AUD = ' + str(zaraud) + ' ZAR'
    return formatted_exchange_data
