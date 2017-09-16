import ConfigParser
import unittest
import telegram

import commands.getquote as getquote


class TestGetQuote(unittest.TestCase):
    def test_getquote(self):
        requestText = 'I will fuck you up'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_PRIVATE_CHAT_ID')

        getquote.run(bot, chatId, 'Admin', keyConfig, requestText)

    def test_getquote_group(self):
        requestText = 'cook pu'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_GROUP_CHAT_ID')

        getquote.run(bot, chatId, 'SalamiArmy', keyConfig, requestText)
