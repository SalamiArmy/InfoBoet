import ConfigParser
import unittest

import telegram

import commands.bitcoin as bitcoin


class TestBitcoin(unittest.TestCase):
    def test_bitcoin(self):
        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_GROUP_CHAT_ID')

        bitcoin.run(bot, chatId, 'Admin', keyConfig)
