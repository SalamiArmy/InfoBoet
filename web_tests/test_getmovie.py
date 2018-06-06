import ConfigParser
import unittest
import telegram

import telegram_commands.getmovie as getmovie


class TestGetMovie(unittest.TestCase):
    def test_getmovie(self):
        requestText = 'Planes, Trains and Automobiles'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_PRIVATE_CHAT_ID')

        bot.sendMessage(chat_id=chatId, text=getmovie.run('Admin', requestText, chatId))
