import ConfigParser
import unittest
import telegram

import commands.urban as urban


class TestUrban(unittest.TestCase):
    def test_urban(self):
        requestText = 'dem titties'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_GROUP_CHAT_ID')

        urban.run(bot, chatId, 'SalamiArmy', keyConfig, requestText)
