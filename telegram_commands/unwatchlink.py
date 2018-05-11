# coding=utf-8
import main
watchlink = main.load_code_as_module('watchlink')

def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    watchlink.unwatch(bot, chat_id, message)


