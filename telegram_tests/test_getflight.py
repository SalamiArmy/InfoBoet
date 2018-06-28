# coding=utf-8
import ConfigParser
import unittest
import telegram

import telegram_commands.getflight as getflight


class TestPlace(unittest.TestCase):
    def test_getairport(self):
        requestText = 'timbuktu'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        keyConfig.read(["bot_keys.ini", "..\\bot_keys.ini"])
        bot = telegram.Bot(keyConfig.get('BotIDs', 'TELEGRAM_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_TELEGRAM_PRIVATE_CHAT_ID')

        getflight.run(bot, chatId, 'Admin', keyConfig, requestText)

    def test_getonewayflight(self):
        requestText = 'DUR DUB 2018-08-15'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        keyConfig.read(["bot_keys.ini", "..\\bot_keys.ini"])
        bot = telegram.Bot(keyConfig.get('BotIDs', 'TELEGRAM_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_TELEGRAM_PRIVATE_CHAT_ID')

        getflight.run(bot, chatId, 'Admin', keyConfig, requestText)

    def test_getreturnflight(self):
        requestText = 'DUR DUB 2019-04-14 2019-04-16'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        keyConfig.read(["bot_keys.ini", "..\\bot_keys.ini"])
        bot = telegram.Bot(keyConfig.get('BotIDs', 'TELEGRAM_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_TELEGRAM_PRIVATE_CHAT_ID')

        getflight.run(bot, chatId, 'Admin', keyConfig, requestText)
