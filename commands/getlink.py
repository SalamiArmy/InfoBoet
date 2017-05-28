# coding=utf-8
import json
import random
import string
import urllib

import telegram

from commands import retry_on_telegram_error


def run(bot, chat_id, user, keyConfig, message, total_requested_results=1):
    requestText = message.replace(bot.name, "").strip()
    googurl = 'https://www.googleapis.com/customsearch/v1'
    args = {'cx': keyConfig.get('Google', 'GCSE_SE_ID'),
            'key': keyConfig.get('Google', 'GCSE_APP_ID'),
            'safe': "off",
            'q': requestText}
    realUrl = googurl + '?' + urllib.urlencode(args)
    data = json.load(urllib.urlopen(realUrl))
    if 'items' in data:
        total_sent = 0
        total_actual_results = int(data['searchInformation']['totalResults'])
        if total_actual_results < total_requested_results:
            total_results_to_send = total_actual_results
            bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                                  ', I\'m afraid I can only find ' + str(total_actual_results) +
                                                  ' links for ' + string.capwords(requestText.encode('utf-8')) + '.')
        else:
            total_results_to_send = total_requested_results
        while total_sent < total_results_to_send:
            imagelink = data['items'][total_sent]['link']
            bot.sendMessage(chat_id=chat_id, text=user + requestText +
                                                  (' ' + str(total_sent + 1) + ' of ' + str(total_results_to_send) if int(total_results_to_send) > 1 else '') +
                                                  ': ' + imagelink)
            total_sent += 1
    else:
        if 'error' in data:
            bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                                  ' I got ' + data['error']['message'] + '.')
        else:
            bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                                  ', I\'m afraid I can\'t find any links for ' +
                                                  string.capwords(requestText.encode('utf-8')))


