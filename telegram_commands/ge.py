import main
getgerman = main.load_code_as_module('getgerman')
def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    getgerman.run(bot, chat_id, user, keyConfig, message, totalResults)
