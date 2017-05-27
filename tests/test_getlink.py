import ConfigParser
import unittest
import telegram

import commands.getlink as getlink


class TestGet(unittest.TestCase):
    def test_get(self):
        requestText = 'missing Russian rpg'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_PRIVATE_CHAT_ID')

        getlink.run(bot, chatId, 'SalamiArmy', keyConfig, requestText, 2)
