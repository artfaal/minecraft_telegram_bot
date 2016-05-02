# -*- coding: utf-8 -*-
from config import TELEGRAM_API, DEBUG
from time import sleep
from telegram.ext import Updater
from hoster import get_balance, action_with, is_server_power_on
from minecraft import get_info, is_minecraft_run
from ssh import stop_minecraft, start_minecraft, free_mem, cpu_load, swap, reboot_cmd


if DEBUG:
    import logging
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s \
                                - %(message)s')


def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text='\xF0\x9F\x98\x81 Приветствую милый друг.Если что не так, пиши мне - @artfaal')


def balance(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text='Баланс счета: %s руб.' % str(get_balance()))


def on(bot, update):
    if is_server_power_on():
        bot.sendMessage(chat_id=update.message.chat_id, text='Сервер уже включен')
    else:
        action_with('PowerOn')
        bot.sendMessage(chat_id=update.message.chat_id, text='Запускаем сервер')


def off(bot, update):
    if is_server_power_on():
        if is_minecraft_run():
            bot.sendMessage(chat_id=update.message.chat_id, text='Сохраняем мир...')
            stop_minecraft()
            sleep(7)
        action_with('PowerOff')
        bot.sendMessage(chat_id=update.message.chat_id, text='Выключаем сервер')
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text='Сервер уже выключен')


def start_script(bot, update):
    if is_server_power_on():
        if is_minecraft_run():
            bot.sendMessage(chat_id=update.message.chat_id, text='Майнкрафт уже запушен')
        else:
            start_minecraft()
            bot.sendMessage(chat_id=update.message.chat_id, text='Активируем скрипт запуска')
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text='Сначала включите сервер')


def stop_script(bot, update):
    if is_server_power_on():
        if is_minecraft_run():
            stop_minecraft()
            bot.sendMessage(chat_id=update.message.chat_id, text='Активируем скрипт завершения')
        else:
            bot.sendMessage(chat_id=update.message.chat_id, text='Майнкрафт уже выключен')
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text='Сначала включите сервер')


def reboot(bot, update):
    if is_server_power_on():
        if is_minecraft_run:
            bot.sendMessage(chat_id=update.message.chat_id, text='Сохраняем мир...')
            stop_minecraft()
            sleep(4)
        reboot_cmd()
        bot.sendMessage(chat_id=update.message.chat_id, text='Перезапускаем сервер')
    else:
        action_with('PowerOn')
        bot.sendMessage(chat_id=update.message.chat_id, text='Сервер был выключен. Включаем')


def server_info(bot, update):
    mem = free_mem()
    cpu = cpu_load()
    swap_file = swap()
    bot.sendMessage(chat_id=update.message.chat_id, text='Free RAM:\n%s KB\n==========\nЗагрузка ядер:\nCPU 1: %s\nCPU 2: %s\nCPU 3: %s\n\n' % (mem, cpu[0], cpu[1], cpu[2]))
    if swap_file > 0:
        bot.sendMessage(chat_id=update.message.chat_id, text='Сервер начал использовать файл подкачки. Желательно перезапустить сервер.\nSwap: %s KB' % swap_file)


def convert_array_to_str(array):
    names = []
    for i in array:
        names.append(i['name'])
    formated_names = str(', '.join(names))
    return formated_names


def status(bot, update):
    if is_server_power_on():
        try:
            json_info = get_info()
            if json_info['online'] == 0:
                bot.sendMessage(chat_id=update.message.chat_id, text='Сервер запущен, но пуст')
            else:
                people_array = json_info['sample']
                bot.sendMessage(chat_id=update.message.chat_id, text='Сервер запущен. Присутствуют: %s.' % convert_array_to_str(people_array))
        except Exception, e:
            bot.sendMessage(chat_id=update.message.chat_id, text='Сервер включен. Но Minecraft не запущен.\nКод ошибки:%s' % e)
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text='Сервер в данный момент выключен')


def unknown(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Таких команд я не знаю... \xF0\x9F\x98\xB1")


updater = Updater(token=TELEGRAM_API)
job_queue = updater.job_queue
dispatcher = updater.dispatcher


def use_commands():
    cmd_list = [start, balance, on, off, start_script, stop_script, reboot, server_info, status]
    for m in cmd_list:
        dispatcher.addTelegramCommandHandler(m.__name__, m)
use_commands()
dispatcher.addUnknownTelegramCommandHandler(unknown)
updater.start_polling()
updater.idle()
job_queue.stop()


# status - Статус Майнкрафта
# server_info - Информация о сервере
# on - Включение сервера
# off - Выключение сервера
# reboot - Перезапуск сервера
# balance - Проверить баланс
# start_script - Скрипт запуска клиента
# stop_script - Скрипт остановки клиента
