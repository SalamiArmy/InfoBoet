# coding=utf-8
import ConfigParser
import unittest
import telegram

import telegram_commands.place as place


class TestPlace(unittest.TestCase):
    def test_place(self):
        requestText = 'Rabbit Hash, Kentucky'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('BotIDs', 'TELEGRAM_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_PRIVATE_CHAT_ID')

        place.run(bot, chatId, 'Admin', keyConfig, requestText)
