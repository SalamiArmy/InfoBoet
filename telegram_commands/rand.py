# coding=utf-8
import json
import urllib


def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    bot.sendMessage(chat_id=chat_id, text=get_exchange_data(keyConfig))
    return True

def get_exchange_data(keyConfig):
    usdurl = 'http://data.fixer.io/api/latest?base=USD&access_key=' + keyConfig.get('Fixer', 'API_KEY')
    gbpurl = 'http://data.fixer.io/api/latest?base=GBP&access_key=' + keyConfig.get('Fixer', 'API_KEY')
    eururl = 'http://data.fixer.io/api/latest?base=EUR&access_key=' + keyConfig.get('Fixer', 'API_KEY')
    data1 = json.load(urllib.urlopen(usdurl))
    data2 = json.load(urllib.urlopen(gbpurl))
    data3 = json.load(urllib.urlopen(eururl))
    zarusd = float(data1['rates']['ZAR'])
    zargbp = float(data2['rates']['ZAR'])
    zareur = float(data3['rates']['ZAR'])
    formatted_exchange_data = '1 USD = ' + str(zarusd) + ' ZAR\n1 GBP = ' + str(zargbp) + ' ZAR\n1 EUR = ' + str(zareur) + ' ZAR'
    return formatted_exchange_data