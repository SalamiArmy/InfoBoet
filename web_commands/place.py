# coding=utf-8
import json
import logging
import urllib

import telegram


def run(keyConfig, message, totalResults=1):
    requestText = message.strip()

    mapsUrl = 'https://maps.googleapis.com/maps/api/place/textsearch/json?key=' + \
              keyConfig.get('Google', 'GCSE_APP_ID') + '&location=-30,30&radius=50000&query='
    realUrl = mapsUrl + requestText
    data = json.load(urllib.urlopen(realUrl))
    logging.info('Place content:')
    logging.info(data)
    if 'results' in data and len(data['results']) > 0:
        latNum = data['results'][0]['geometry']['location']['lat']
        lngNum = data['results'][0]['geometry']['location']['lng']
        return 'lat=' + latNum + ' and long=' + lngNum
    else:
        errorMessage = ''
        if 'error_message' in data:
            errorMessage = data['error_message']
        if 'status' in data:
            errorMessage = data['status']
        return 'I\'m sorry Dave, ' + errorMessage