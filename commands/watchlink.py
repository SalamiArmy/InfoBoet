# coding=utf-8
import string

import main
getlink = main.load_code_as_module('getlink')

def run(bot, chat_id, user, keyConfig, message, num_to_send=1):
    requestText = message.replace(bot.name, "").strip()
    args = {'cx': keyConfig.get('Google', 'GCSE_OTHER_SE_ID'),
            'key': keyConfig.get('Google', 'GCSE_APP_ID'),
            'safe': 'off',
            'q': requestText}
    single_page_watch(args, bot, chat_id, keyConfig, requestText, user, 'getlink')

def unwatch(bot, chat_id, message):
    watches = main.getAllWatches()
    if ',' + str(chat_id) + ':' + getlink.CommandName + ':' + message + ',' in watches or \
            watches.startswith(str(chat_id) + ':' + getlink.CommandName + ':' + message + ',') or \
            watches.endswith(',' + str(chat_id) + ':' + getlink.CommandName + ':' + message) or \
                    watches == str(chat_id) + ':' + getlink.CommandName + ':' + message:
        main.removeFromAllWatches(str(chat_id) + ':' + getlink.CommandName + ':' + message)
        bot.sendMessage(chat_id=chat_id, text='Watch for /' + getlink.CommandName + ' ' + message + ' has been removed.')
    else:
        bot.sendMessage(chat_id=chat_id, text='Watch for /' + getlink.CommandName + ' ' + message + ' not found.')

def single_page_watch(args, bot, chat_id, keyConfig, requestText, user, CommandName):
    data, total_results, results_this_page = getlink.Google_Custom_Search(args)
    if 'items' in data and results_this_page >= 0:
        offset_this_page = 0
        total_sent = 0
        while offset_this_page < results_this_page:
            link = data['items'][offset_this_page]['link']
            offset_this_page += 1
            if user != 'Watcher':
                if total_sent == 0 and not main.AllWatchesContains(CommandName, chat_id, requestText):
                    watch_message = 'Now watching /' + CommandName + ' ' + requestText + '.'
                else:
                    watch_message = 'Watched /' + CommandName + ' ' + requestText + ' changed' + '.'
                bot.sendMessage(chat_id=chat_id, text=watch_message + '\n' + link)
                total_sent += 1
            else:
                bot.sendMessage(chat_id=chat_id, text='Watched /' + CommandName + ' ' + requestText + ' changed.' +
                                                      '\n' + link)
                total_sent += 1
        if total_sent == 0:
            if user != 'Watcher':
                bot.sendMessage(chat_id=chat_id, text=user + ', watch for /' + CommandName + ' ' + requestText +
                                                      ' has not changed.')
        if not main.AllWatchesContains(CommandName, chat_id, requestText):
            main.addToAllWatches(CommandName, chat_id, requestText)
    else:
        if user != 'Watcher':
            bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                                  ', I\'m afraid I can\'t find any results for /' +
                                                  CommandName + ' ' +
                                                  string.capwords(requestText.encode('utf-8')))