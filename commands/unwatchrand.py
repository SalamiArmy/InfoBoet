# coding=utf-8
import main
watchrand = main.load_code_as_module('watchrand')

def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    watchrand.unwatch(bot, chat_id, message)


