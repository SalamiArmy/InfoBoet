import ConfigParser
import requests
import telegram


# http://api.funtranslations.com/translate/yoda.json?text=
def translate(msg):
    r = requests.get("http://api.funtranslations.com/translate/yoda.json?text=" + msg)
    if r.status_code == 429:
        return "Sorry I can only translate 5 times per hour"
    try:
        return r.json()['contents']['translated'].replace("  ", " ")
    except:
        print(r.text)
        return "An unexpected error occurred"

def run(keyConfig, message, totalResults=1):
    keyConfig = ConfigParser.ConfigParser()
    keyConfig.read(["keys.ini", "..\keys.ini"])
    return translate(message)
