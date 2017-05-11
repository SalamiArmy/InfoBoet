import ConfigParser
import unittest
import telegram

import commands.reverseimage as reverseimage


class TestReverseImage(unittest.TestCase):
    def test_reverseimage(self):
        requestText = 'https://s-media-cache-ak0.pinimg.com/originals/e3/68/e2/e368e259e24b47d3b61eeed92a2e1b0d.gif'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))

        #for admin group
        chatId = keyConfig.get('BotAdministration', 'TESTING_GROUP_CHAT_ID')

        reverseimage.run(bot, chatId, 'Admin', keyConfig, requestText)
