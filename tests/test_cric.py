# coding=utf-8
import ConfigParser
import unittest
import telegram

import telegram_commands.cric as cric


class TestCric(unittest.TestCase):
    def test_cric(self):
        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_PRIVATE_CHAT_ID')

        cric.run(bot, chatId, 'Admin', keyConfig, '')
