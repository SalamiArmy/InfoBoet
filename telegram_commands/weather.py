
import datetime
import json
import urllib
import uuid

import telegram


def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    requestText = message.replace(bot.name, "").strip()
    url = 'https://sawx.co.za/clouds/south-africa-live-animated-satellite-clouds-stream-radar-rainfall-maps/south-africa-clouds-stream-live-animated-satellite-radar-weather-map.gif&uuid=' + \
          str(uuid.uuid4())
    bot.sendMessage(chat_id=chat_id, text=url)
