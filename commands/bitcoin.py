# coding=utf-8
import json
import urllib
import logging


def run(bot, chat_id, user, keyConfig, message="", totalResults=1):
    priceGB, priceUS, priceZA, updateTime = get_bitcoin_prices()
    bot.sendMessage(chat_id=chat_id,
                    text='The Current Price of 1 Bitcoin:\n\n' + priceUS +
                         ' USD\n' + priceGB +
                         ' GBP\n' + priceZA + ' ZAR' + '\n\nTime Updated: ' + updateTime)
    return True


def get_bitcoin_prices():
    bcurl = 'https://api.coindesk.com/v1/bpi/currentprice/ZAR.json'
    RAW_DATA = urllib.urlopen(bcurl)
    logging.info('raw bitcoin data returned as: ' + RAW_DATA)
    if RAW_DATA:
        data = json.load(RAW_DATA)
        bcurl2 = 'https://api.coindesk.com/v1/bpi/currentprice.json'
        rawJSON = urllib.urlopen(bcurl2)
        try:
            data2 = json.load(rawJSON)
            updateTime = data['time']['updated']
            priceUS = data['bpi']['USD']['rate']
            priceZA = data['bpi']['ZAR']['rate']
            priceGB = data2['bpi']['GBP']['rate']
            return priceGB, priceUS, priceZA, updateTime
        except ValueError:
            print('Value error: ' + rawJSON.read)
    else:
        print('raw bitcoin data returned nothing.')
