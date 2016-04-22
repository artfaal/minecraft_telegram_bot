# -*- coding: utf-8 -*-
from config import TELEGRAM_API
import logging
from telegram.ext import Updater
from hoster import get_balance, action_with
from minecraft import get_info
import re

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
    action_with('PowerOff')
    bot.sendMessage(chat_id=update.message.chat_id, text='Выключаем сервер')


def reboot(bot, update):
    action_with('PowerReboot')
    bot.sendMessage(chat_id=update.message.chat_id, text='Перезапускаем сервер')


def status(bot, update):
    try:
        r = get_info()
        try:
            people_array = r['sample']
            people = []
            for i in people_array:
                people.append(i['name'])
            a = str(', '.join(people))
            print type(a)
            bot.sendMessage(chat_id=update.message.chat_id, text='Сервер запущен. Присутствуют: %s.' % a)
        except Exception, e:
            bot.sendMessage(chat_id=update.message.chat_id, text='Сервер запущен, но пуст')
            pass
    except Exception, e:
        bot.sendMessage(chat_id=update.message.chat_id, text='Сервер недоступен\nКод ошибки:%s' % e)


def unknown(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Таких команд я не знаю... \xF0\x9F\x98\xB1")


updater = Updater(token=TELEGRAM_API)
job_queue = updater.job_queue
dispatcher = updater.dispatcher
dispatcher.addTelegramCommandHandler('start', start)
dispatcher.addTelegramCommandHandler('balance', balance)
dispatcher.addTelegramCommandHandler('on', on)
dispatcher.addTelegramCommandHandler('off', off)
dispatcher.addTelegramCommandHandler('reboot', reboot)
dispatcher.addTelegramCommandHandler('status', status)
dispatcher.addUnknownTelegramCommandHandler(unknown)
updater.start_polling()
updater.idle()
job_queue.stop()
