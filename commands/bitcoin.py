import main
getfig = main.load_code_as_module('getfig')
def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    getfig.run(bot, chat_id, user, keyConfig, message, totalResults)