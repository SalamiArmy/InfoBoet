import ConfigParser
import unittest
import telegram

import telegram_commands.getmovie as getmovie


class TestGetMovie(unittest.TestCase):
    def test_getmovie(self):
        requestText = 'Planes, Trains and Automobiles'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        keyConfig.read(["bot_keys.ini", "..\\bot_keys.ini"])
        bot = telegram.Bot(keyConfig.get('BotIDs', 'TELEGRAM_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_TELEGRAM_PRIVATE_CHAT_ID')

        getmovie.run(bot, chatId, 'Admin', keyConfig, requestText)
