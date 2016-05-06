# -*- coding: utf-8 -*-
from config import TELEGRAM_API, DEBUG
from time import sleep
from telegram.ext import Updater
from telegram import ParseMode
from hoster import get_balance, power_on_instance, power_off_instance
from minecraft import get_info, is_minecraft_run
from ssh import stop_minecraft, start_minecraft, free_mem, cpu_load, swap, reboot_cmd, get_log, shutdown_cmd, is_server_on


if DEBUG:
    import logging
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s \
                                - %(message)s')

# CONSTANT
SLEEP_TIME = 10


def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text='\xF0\x9F\x98\x81 Приветствую милый друг.Если что не так, пиши мне - @artfaal')


def balance(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text='Баланс счета: %s руб.' % str(get_balance()))


def on(bot, update):
    if is_server_on():
        bot.sendMessage(chat_id=update.message.chat_id, text='Сервер уже включен')
    else:
        power_on_instance()
        bot.sendMessage(chat_id=update.message.chat_id, text='Запускаем сервер')


def off(bot, update):
    if is_server_on():
        if is_minecraft_run():
            bot.sendMessage(chat_id=update.message.chat_id, text='Сохраняем мир...')
            stop_minecraft()
            sleep(SLEEP_TIME)
            minecraft_latest_log(bot, update)
        shutdown_cmd()
        power_off_instance()
        bot.sendMessage(chat_id=update.message.chat_id, text='Выключаем сервер')
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text='Сервер уже выключен')


def start_script(bot, update):
    if is_server_on():
        if is_minecraft_run():
            bot.sendMessage(chat_id=update.message.chat_id, text='Майнкрафт уже запушен')
        else:
            start_minecraft()
            bot.sendMessage(chat_id=update.message.chat_id, text='Активируем скрипт запуска')
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text='Сначала включите сервер')


def stop_script(bot, update):
    if is_server_on():
        if is_minecraft_run():
            stop_minecraft()
            bot.sendMessage(chat_id=update.message.chat_id, text='Активируем скрипт завершения')
        else:
            bot.sendMessage(chat_id=update.message.chat_id, text='Майнкрафт уже выключен')
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text='Сначала включите сервер')


def reboot(bot, update):
    if is_server_on():
        if is_minecraft_run():
            bot.sendMessage(chat_id=update.message.chat_id, text='Сохраняем мир...')
            stop_minecraft()
            sleep(SLEEP_TIME)
            minecraft_latest_log(bot, update)
        bot.sendMessage(chat_id=update.message.chat_id, text='Перезапускаем сервер')
        reboot_cmd()
    else:
        power_on_instance()
        bot.sendMessage(chat_id=update.message.chat_id, text='Сервер был выключен. Включаем')


def convert_array_to_str(array):
    names = []
    for i in array:
        names.append(i['name'])
    formated_names = str(', '.join(names))
    return formated_names


def server_info(bot, update):
    mem = free_mem()
    cpu = cpu_load()
    swap_file = swap()
    bot.sendMessage(chat_id=update.message.chat_id, text='Free RAM:\n%s KB\n==========\nЗагрузка ядер:\nCPU 1: %s\nCPU 2: %s\nCPU 3: %s\n\n' % (mem, cpu[0], cpu[1], cpu[2]))
    if swap_file > 0:
        bot.sendMessage(chat_id=update.message.chat_id, text='Сервер начал использовать файл подкачки. Желательно перезапустить сервер.\nSwap: %s KB' % swap_file)


def status(bot, update):
    try:
        json_info = get_info()
        if json_info['online'] == 0:
            bot.sendMessage(chat_id=update.message.chat_id, text='Сервер запущен, но пуст')
        else:
            people_array = json_info['sample']
            bot.sendMessage(chat_id=update.message.chat_id, text='Сервер запущен. Присутствуют: %s.' % convert_array_to_str(people_array))
    except Exception, e:
        bot.sendMessage(chat_id=update.message.chat_id, text='Сервер включен. Но Minecraft не запущен.\nКод ошибки:%s' % e)


def global_info(bot, update):
    if is_server_on():
        status(bot, update)
        server_info(bot, update)
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text='Сервер в данный момент выключен')


def minecraft_latest_log(bot, update):
    log = get_log()
    bot.sendMessage(chat_id=update.message.chat_id, text="```\n %s \n```" % log, parse_mode=ParseMode.MARKDOWN)


def unknown(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Таких команд я не знаю... \xF0\x9F\x98\xB1")


updater = Updater(token=TELEGRAM_API)
job_queue = updater.job_queue
dispatcher = updater.dispatcher


def use_commands():
    cmd_list = [start, balance, on, off, start_script, stop_script, reboot, global_info, minecraft_latest_log]
    for m in cmd_list:
        dispatcher.addTelegramCommandHandler(m.__name__, m)
use_commands()
dispatcher.addUnknownTelegramCommandHandler(unknown)
updater.start_polling()
updater.idle()
job_queue.stop()

"""
Autocomplete commands. Sent it to @BotFather
/setcommands

global_info - Общая информация о сервере
minecraft_latest_log - Лог майнкрафта
on - Включение сервера
off - Выключение сервера
reboot - Перезапуск сервера
balance - Проверить баланс
start_script - Скрипт запуска клиента
stop_script - Скрипт остановки клиента
"""
