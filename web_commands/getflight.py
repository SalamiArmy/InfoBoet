# coding=utf-8
import urllib
from bs4 import BeautifulSoup

import main
telegramgetflight = main.get_platform_command_code('telegram', 'getflight')

def run(keyConfig, message, totalResults=1):
    requestText = message.strip()
    if (requestText[3] == " " and requestText[7] == " " and requestText[12] == "-" and requestText[15] == "-"):
        flightData = telegramgetflight.get_flights(requestText)
        if flightData != '':
            return flightData
        else:
            return 'I\'m sorry Dave, I\'m afraid I can\'t find any one way flights for ' + str(requestText) + '.'
    else:
        airportCode, error = telegramgetflight.get_airport_code(requestText)
        if airportCode != 'No matching entries found...':
            return airportCode
        else:
            if error:
                return 'I\'m sorry Dave' + error
            else:
                return 'I\'m sorry Dave, I\'m afraid I can\'t quite place ' + str(requestText) + '.'
