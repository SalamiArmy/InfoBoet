# coding=utf-8
import main
watchbitcoin = main.load_code_as_module('watchbitcoin')

def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    watchbitcoin.unwatch(bot, chat_id, message, True)
