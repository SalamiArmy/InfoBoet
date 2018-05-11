import main
pronounce = main.load_code_as_module('pronounce')
def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    pronounce.run(bot, chat_id, user, keyConfig, message, totalResults)
