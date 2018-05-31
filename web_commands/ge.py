import main
getgerman = main.get_platform_command_code('web', 'getgerman')
def run(keyConfig, message, totalResults=1):
    getgerman.run(keyConfig, message, totalResults)
