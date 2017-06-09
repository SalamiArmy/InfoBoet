import ConfigParser
import unittest
import telegram

import commands.getsuggestion as getsuggestion


class TestGet(unittest.TestCase):
    def test_get(self):
        requestText = 'how to'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_PRIVATE_CHAT_ID')

        getsuggestion.run(bot, chatId, 'Admin', keyConfig, requestText)
