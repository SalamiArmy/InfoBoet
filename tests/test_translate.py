# coding=utf-8
import ConfigParser
import unittest
import telegram

import commands.translate as translate


class TestTorrent(unittest.TestCase):
    def test_translate_in_group_chat(self):
        requestText = 'Deutsche Vermögensberatung'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_GROUP_CHAT_ID')

        translate.run(bot, chatId, 'Admin', keyConfig, requestText)

    def test_translate_in_private_chat(self):
        requestText = 'Deutsche Vermögensberatung'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_PRIVATE_CHAT_ID')

        translate.run(bot, chatId, 'Admin', keyConfig, requestText)
