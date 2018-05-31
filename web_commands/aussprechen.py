import main
pronounce = main.get_platform_command_code('web', 'pronounce')
def run(keyConfig, message, totalResults=1):
    pronounce.run(keyConfig, message, totalResults)
