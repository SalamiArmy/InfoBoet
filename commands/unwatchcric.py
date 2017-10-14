# coding=utf-8
import main
watchcric = main.load_code_as_module('watchbitcoin')

def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    watchcric.unwatch(bot, chat_id, message)


