# coding=utf-8
import json
import urllib


def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    bot.sendMessage(chat_id=chat_id, text='Started.')
