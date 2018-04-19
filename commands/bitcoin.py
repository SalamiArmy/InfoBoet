# coding=utf-8
import json

from google.appengine.api import urlfetch

def run(bot, chat_id, user, keyConfig, message="", totalResults=1):
    tickers = ['BTC',
               'ETH',
               'XRP',
               'BCH',
               'LTC',
               'EOS',
               'ADA',
               'XLM',
               'NEO',
               'IOTA',
               'XMR',
               'XEM',
               'DASH',
               'TRX']
    for ticker in tickers:
        bcurl = 'https://min-api.cryptocompare.com/data/price?fsym=' + ticker + '&tsyms=ZAR,USD,EUR'
        RAW_DATA = urlfetch.fetch(bcurl)
        data = json.loads(RAW_DATA.content)
        bot.sendMessage(chat_id=chat_id,
                        text='The Current Price of 1 ' + ticker + ':\n\n' + data['USD'] +
                             ' USD\n' + data['EUR'] +
                             ' EUR\n' + data['ZAR'] + ' ZAR')
    return True
        
