# coding=utf-8
import ConfigParser
import unittest

import telegram

import telegram_commands.define as define


class TestDefine(unittest.TestCase):
    def test_define_private(self):
        requestText = 'great'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        keyConfig.read(["bot_keys.ini", "..\\bot_keys.ini"])
        bot = telegram.Bot(keyConfig.get('BotIDs', 'TELEGRAM_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_TELEGRAM_PRIVATE_CHAT_ID')

        define.run(bot, chatId, 'SalamiArmy', keyConfig, requestText)
