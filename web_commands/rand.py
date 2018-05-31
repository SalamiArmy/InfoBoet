# coding=utf-8
import json
import urllib


def run(keyConfig, message, totalResults=1):
    return get_exchange_data()

def get_exchange_data():
    usdurl = 'http://api.fixer.io/latest?base=USD'
    gbpurl = 'http://api.fixer.io/latest?base=GBP'
    eururl = 'http://api.fixer.io/latest?base=EUR'
    data1 = json.load(urllib.urlopen(usdurl))
    data2 = json.load(urllib.urlopen(gbpurl))
    data3 = json.load(urllib.urlopen(eururl))
    zarusd = float(data1['rates']['ZAR'])
    zargbp = float(data2['rates']['ZAR'])
    zareur = float(data3['rates']['ZAR'])
    formatted_exchange_data = '1 USD = ' + str(zarusd) + ' ZAR\n1 GBP = ' + str(zargbp) + ' ZAR\n1 EUR = ' + str(zareur) + ' ZAR'
    return formatted_exchange_data