# coding=utf-8
import urllib
from bs4 import BeautifulSoup

import main
telegramgetflight = main.get_platform_command_code('telegram', 'getflight')

def run(keyConfig, message, totalResults=1):
    requestText = message.strip()
    if (requestText[3] == " " and requestText[7] == " " and requestText[12] == "-" and requestText[15] == "-" and len(requestText) > 19 and requestText[18] == " " and requestText[23] == "-" and requestText[26] == "-"):
        return telegramgetflight.get_returnflights(requestText)
    else:
        if (requestText[3] == " " and requestText[7] == " " and requestText[12] == "-" and requestText[15] == "-"):
            return telegramgetflight.get_flights(requestText)
        else:
            airportCode, error = telegramgetflight.get_airport_code(requestText)
            if airportCode != '':
                return airportCode
            else:
                if error:
                    return 'I\'m sorry Dave, ' + error
                else:
                    return 'I\'m sorry Dave, I\'m afraid I can\'t quite place ' + str(requestText) + '.'
