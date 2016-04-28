# -*- coding: utf-8 -*-
from config import TELEGRAM_API
import logging
from time import sleep
from telegram.ext import Updater
from hoster import get_balance, action_with
from minecraft import get_info
from ssh import stop_minecraft

# logging.basicConfig(level=logging.DEBUG,
#                     format='%(asctime)s - %(name)s - %(levelname)s \
#                             - %(message)s')


def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text='\xF0\x9F\x98\x81 Приветствую милый друг.Если что не так, пиши мне - @artfaal')


def balance(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text='Баланс счета: %s руб.' % str(get_balance()))


def on(bot, update):
    action_with('PowerOn')
    bot.sendMessage(chat_id=update.message.chat_id, text='Запускаем сервер')


def off(bot, update):
    stop_minecraft()
    bot.sendMessage(chat_id=update.message.chat_id, text='Сохраняем мир...')
    sleep(7)
    action_with('PowerOff')
    bot.sendMessage(chat_id=update.message.chat_id, text='Выключаем сервер')


def reboot(bot, update):
    stop_minecraft()
    bot.sendMessage(chat_id=update.message.chat_id, text='Сохраняем мир...')
    sleep(7)
    action_with('PowerReboot')
    bot.sendMessage(chat_id=update.message.chat_id, text='Перезапускаем сервер')


def convert_array_to_str(array):
    names = []
    for i in array:
        names.append(i['name'])
    formated_names = str(', '.join(names))
    return formated_names


def status(bot, update):
    try:
        raw_json_info = get_info()
        try:
            people_array = raw_json_info['sample']
            bot.sendMessage(chat_id=update.message.chat_id, text='Сервер запущен. Присутствуют: %s.' % convert_array_to_str(people_array))
        except Exception, e:
            bot.sendMessage(chat_id=update.message.chat_id, text='Сервер запущен, но пуст')
    except Exception, e:
        bot.sendMessage(chat_id=update.message.chat_id, text='Сервер недоступен\nКод ошибки:%s' % e)


def unknown(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Таких команд я не знаю... \xF0\x9F\x98\xB1")


updater = Updater(token=TELEGRAM_API)
job_queue = updater.job_queue
dispatcher = updater.dispatcher


def use_commands():
    cmd_list = [start, balance, on, off, reboot, status]
    for m in cmd_list:
        dispatcher.addTelegramCommandHandler(m.__name__, m)
use_commands()
dispatcher.addUnknownTelegramCommandHandler(unknown)
updater.start_polling()
updater.idle()
job_queue.stop()
