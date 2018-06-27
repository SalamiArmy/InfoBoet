# coding=utf-8
import ConfigParser
import unittest
import telegram

import telegram_commands.getflight as getflight


class TestPlace(unittest.TestCase):
    def test_getflight(self):
        requestText = 'lucerne'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        keyConfig.read(["bot_keys.ini", "..\\bot_keys.ini"])
        bot = telegram.Bot(keyConfig.get('BotIDs', 'TELEGRAM_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_TELEGRAM_PRIVATE_CHAT_ID')

        getflight.run(bot, chatId, 'Admin', keyConfig, requestText)
