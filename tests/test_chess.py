import ConfigParser
import unittest

import telegram

import telegram_commands.chess as chess


class TestChess(unittest.TestCase):
    def test_chess(self):
        requestText = '@Bashs_Bot bitcoin'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_PRIVATE_CHAT_ID')

        chess.run(bot, chatId, 'Admin', keyConfig, requestText)
