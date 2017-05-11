# InfoBoet
## A simple python bot for Telegram who knows things and stuff.

### What is InfoBoet?
InfoBoet is a chat bot for telegram that talks to you. You can even add new commands while he's running!

### How does it work?
InfoBoet will listen for all messages in a given chat (either directly with him or in a chat room which you invite him to) but explicit commands start with "/".

### How do I make my own bot using this?
Go to https://console.developers.google.com and create a Google App Engine project. Then take that project id (it will be two random words and a number eg. gorilla-something-374635) and your Telegram Bot ID which the Bot Father gave you and do the following:

1. Copy app.yaml.template and rename the copy to to app.yaml.
2. Update {GOOGLE APP ENGINE PROJECT ID} in app.yaml.
3. Copy keys.ini.template and rename the copy to keys.ini.
4. Update {Your Telegram Bot ID here} in keys.ini 
OPTIONAL:
5. Update the rest of keys.ini with keys for each command you want to use.

```bash
git clone (url for your InfoBoet fork) ~/bot
cd ~/bot
(PATH TO PYTHON27 INSTALL)\scripts\pip.exe install -t lib python-telegram-bot bs4 xmltodict six soundcloud feedparser requests tungsten mcstatus google-api-python-client
(PATH TO GOOGLE APP ENGINE LAUNCHER INSTALL)appcfg.py -A {GOOGLE APP ENGINE PROJECT ID} update .
```

Clone from https://github.com/SalamiArmy/TelegramSteamBotForGoogleAppEngine and copy all its commands from it's commands folder into the commands folder.
In lib\SoundCloud\Client.py set enable_ssl = False (Unsupported by Google App Engine)
oh ja, /launch command needs a module called "dateutil" clone from https://github.com/dateutil/dateutil and copy the folder "dateutil" into lib.
See file "pre-push" for an example deploy script.

Finally go to https://{GOOGLE APP ENGINE PROJECT ID}.appspot.com/set_webhook?url=https://{GOOGLE APP ENGINE PROJECT ID}.appspot.com/webhook (replace both {GOOGLE APP ENGINE PROJECT ID}s with the Google App Engine Project ID) to tell Telegram where to send web hooks. This is all that is required to setup web hooks, you do not need to tell the Bot Father anything about web hooks.
