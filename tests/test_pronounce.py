# coding=utf-8
import ConfigParser
import unittest
import telegram

import commands.pronounce as pronounce


class TestTorrent(unittest.TestCase):
    def test_translate(self):
        requestText = 'Neuigkeiten'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_PRIVATE_CHAT_ID')

        pronounce.run(bot, chatId, 'Admin', keyConfig, requestText)
