import ConfigParser
import unittest
import telegram

import commands.launch as launch


class TestLaunch(unittest.TestCase):
    def test_launch(self):
        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        keyConfig.read(["bot_keys.ini", "..\\bot_keys.ini"])
        bot = telegram.Bot(keyConfig.get('BotIDs', 'TELEGRAM_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_TELEGRAM_PRIVATE_CHAT_ID')

        launch.run(bot, chatId, 'Admin', keyConfig, '')
