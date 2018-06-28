# coding=utf-8
import json
import urllib

import telegram
from bs4 import BeautifulSoup


def run(keyConfig, message, totalResults=1):
    requestText = message.strip()
    airportCode, error = get_airport_code(requestText)
    if airportCode != 'No matching entries found...':
        return airportCode
    else:
        if error:
            return 'I\'m sorry Dave' + error
        else:
            return 'I\'m sorry Dave, I\'m afraid I can\'t quite place ' + str(requestText) + '.'


def get_airport_code(cityName):
    airportsUrl = 'http://www.webflyer.com/travel/milemarker/getmileage_ft.cgi?city='
    realUrl = airportsUrl + cityName.encode('utf-8')
    code = urllib.urlopen(realUrl).read()
    data = BeautifulSoup(code, 'html.parser')
    error = data.find('b').string
    rawAirportCode = str(data.findAll('b')[1]) if error != 'No matching entries found...' else ''
    airportCode = rawAirportCode[4:rawAirportCode.index(')<br/>')] if len(rawAirportCode) > 13 else ''
    return airportCode, error.replace('Here are the results of your search:', '')