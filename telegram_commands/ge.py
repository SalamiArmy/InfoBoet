import main
getgerman = main.get_platform_command_code('telegram', 'getgerman')
def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    getgerman.run(bot, chat_id, user, keyConfig, message, totalResults)
