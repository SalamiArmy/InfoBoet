# coding=utf-8
import json
import urllib


def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    bot.sendMessage(chat_id=chat_id, text=get_cric_data(user))

def get_cric_data(user):
    allMatchesUrl = 'http://cricscore-api.appspot.com/csa'
    return 'I\'m sorry ' + (user if not user == '' else 'Dave') + ', I\'m afraid the /cric command is broken right now because ' + allMatchesUrl + ' is down.'

