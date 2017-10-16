# coding=utf-8
import main
watchmc = main.load_code_as_module('watchmc')

def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    watchmc.unwatch(bot, chat_id, message)


