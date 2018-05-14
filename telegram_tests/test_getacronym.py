import ConfigParser
import unittest

import telegram

import telegram_commands.getacronym as getacronym


class TestGetGame(unittest.TestCase):
    def test_getgame(self):
        requestText = 'BBHMM'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('BotIDs', 'TELEGRAM_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_TELEGRAM_PRIVATE_CHAT_ID')

        getacronym.run(bot, chatId, 'Admin', keyConfig, requestText)
