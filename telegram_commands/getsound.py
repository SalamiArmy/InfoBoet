# coding=utf-8
import ConfigParser
import json
import urllib
import urllib2

def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +\
       ', I\'m afraid the soundcloud API is giving me an unauthorized exception. /getsound will be back online once I have fixed this bug.')
