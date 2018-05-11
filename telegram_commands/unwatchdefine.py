# coding=utf-8
import main
watchdefine = main.load_code_as_module('watchdefine')

def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    watchdefine.unwatch(bot, chat_id, message)


