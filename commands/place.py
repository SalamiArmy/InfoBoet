# coding=utf-8
import json
import logging
import urllib

import telegram


def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    requestText = message.replace(bot.name, "").strip()

    bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.FIND_LOCATION)
    mapsUrl = 'https://maps.googleapis.com/maps/api/place/textsearch/json?key=' + \
              keyConfig.get('Google', 'GCSE_APP_ID') + '&location=-30,30&radius=50000&query='
    realUrl = mapsUrl + requestText
    data = json.load(urllib.urlopen(realUrl))
    if 'results' in data and len(data['results']) > 0:
        latNum = data['results'][0]['geometry']['location']['lat']
        lngNum = data['results'][0]['geometry']['location']['lng']
        bot.sendLocation(chat_id=chat_id, latitude=latNum, longitude=lngNum)
        return True
    else:
        logging.info('Place content:')
        logging.info(data)
        if 'error_message' in data:
            bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                                  ', ' + data['error_message'])