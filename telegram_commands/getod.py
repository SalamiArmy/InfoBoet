# coding=utf-8
import ConfigParser
import json
import string
import urllib
from google.appengine.ext import ndb
from google.appengine.api import urlfetch
import main
getlink = main.get_platform_command_code('telegram', 'getlink')

def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    requestText = '+(.mkv|.mp4|.avi|.mov|.mpg|.wmv)  ' + str(message).strip() + '  intitle:"index of" -inurl:(jsp|pl|php|html|aspx|htm|cf|shtml) -inurl:(listen77|mp3raid|mp3toss|mp3drug|index_of|wallywashis)'
    keyConfig = ConfigParser.ConfigParser()
    keyConfig.read(["keys.ini", "..\keys.ini"])

    args = {'cx': keyConfig.get('Google', 'GCSE_OTHER_SE_ID'),
            'key': keyConfig.get('Google', 'GCSE_APP_ID'),
            'safe': "off",
            'q': requestText}
    bot.sendMessage(chat_id=chat_id, text=getlink.Send_Links(chat_id, user, str(message).strip(), args, keyConfig, totalResults))
