# coding=utf-8
import json
import urllib

import telegram


def run(keyConfig, message, totalResults=1):
    requestText = message.strip()


    yahoourl = \
        "https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20" \
        "in%20(select%20woeid%20from%20geo.places(1)%20where%20text%3D%27" + requestText.encode(
            'utf-8') + "%27)%20" \
                       "and%20u%3D%27c%27&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys"
    result = urllib.urlopen(yahoourl).read()
    data = json.loads(result)
    if data['query']['count'] >= 1 and 'item' in data['query']['results']['channel']:
        weather = data['query']['results']['channel']['item']['condition']
        forecast = data['query']['results']['channel']['item']['forecast']
        city = data['query']['results']['channel']['location']['city']
        astronomy = data['query']['results']['channel']['astronomy']
        return ('It is currently ' + weather['text'] + ' in ' + city +
                              ' with a temperature of ' + weather['temp'] + 'C.\nA high of ' +
                              forecast[0]['high'] + ' and a low of ' + forecast[0]['low'] +
                              ' are expected during the day with conditions being ' +
                              forecast[0]['text'] + '.\nSunrise: ' + astronomy['sunrise'] +
                              '\nSunset: ' + astronomy['sunset'])
    else:
        return 'I\'m sorry Dave, I\'m afraid I don\'t know the place ' + str(requestText) + '.'
