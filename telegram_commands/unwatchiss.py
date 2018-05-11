# coding=utf-8
import main
watchiss = main.load_code_as_module('watchiss')

def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    watchiss.unwatch(bot, chat_id, message, True)
