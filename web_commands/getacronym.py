# coding=utf-8
import urllib

import main
telegram_getacronym = main.get_platform_command_code('telegram', 'getacronym')

def run(keyConfig, message, totalResults=1):
    requestText = message.strip().upper()

    code = urllib.urlopen('http://www.abbreviations.com/' + requestText).read()
    resultsList = telegram_getacronym.acronym_results_parser(code)
    if resultsList:
        return acronym_results_printer(requestText, resultsList)
    else:
        return 'I\'m sorry Dave, I\'m afraid I can\'t find the acronym *' + str(requestText) + '*'

def acronym_results_printer(request, list):
    AllGameDetailsFormatted = str(request) + ' could mean:'
    for item in list:
        AllGameDetailsFormatted += '\n' + str(item).replace('Definition', '')
    return AllGameDetailsFormatted