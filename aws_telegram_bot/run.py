# -*- coding: utf-8 -*-

from config import *
from telegram import Updater
import telegram
import logging
from handlers import minecraft
import datetime
import time

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s \
                            - %(message)s')

# Тик проверки сервера на доступность перед запуском
tick = 0
# Максимальное количество итераций
maxtic = 40

TIMEZONE = 3

def datetime_aws(input):
    raw = str(input)[:-6]
    return datetime.datetime.strptime(raw, '%Y-%m-%d %H:%M:%S') + datetime.timedelta(hours=TIMEZONE)


def ago(input):
    instance = datetime_aws(input)
    now = datetime.datetime.now()
    return now - instance

# Minecraft init
minecraft = minecraft.McServer(MINECRAFT_ADDR)


def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text='\xF0\x9F\x98\x81 Приветствую милый друг. Это бот. Ты можешь добавить его к себе в контакты и писать ему лично. Или можешь просто писать ему в группу. Доступные команды: \n/run_server - Запускает сервер\n/stop_server - Останавливает сервер \n/status - Показывает статус сервера\nДумаю, функционал будет наращиваться, но пока так. =) Если что не так, пиши мне - @artfaal')


# def run_server(bot, update):
#     start_server_time = datetime.datetime.now()
#     try:
#         i.start()
#         bot.sendMessage(chat_id=update.message.chat_id,
#                         text='\xF0\x9F\x9A\x80 Запускаем сервер. Напишу, как будет готово ;)')

#         def check_server():
#             global tick
#             time.sleep(10)
#             try:
#                 if minecraft.Update().available:
#                     bot.sendMessage(chat_id=update.message.chat_id,
#                                     text='\xE2\x9C\x85 Готово. Можно заходить на сервер. Запущен в *%s*. Время запуска - *%s*' % (datetime.datetime.now().strftime("%H:%M:%S"), str(datetime.datetime.now() - start_server_time)[:-7]),
#                                     parse_mode=telegram.ParseMode.MARKDOWN)
#                     tick = 0
#                 elif tick >= maxtic:
#                     bot.sendMessage(chat_id=update.message.chat_id,
#                                     text='\xE2\x9D\x97 Не запустился сервер. Что-то не так. Пишите @artfaal')
#                     tick = 0
#                 else:
#                     tick += 1
#                     job_queue.put(check_server(), 10, repeat=False)
#             # Ловим забавную ошибку, которая вызывает креш если отправить запрос перед самой инициализацией. Ставим слип. Ждем и повотор.
#             except TypeError:
#                 tick += 1
#                 job_queue.put(check_server(), 10, repeat=False)

#         check_server()
#     except botocore.exceptions.ClientError as e:
#         bot.sendMessage(chat_id=update.message.chat_id,
#                         text='\xE2\x98\x9D *Скорее всего сервер УЖЕ запущен*. Вот ошибка: %s' % e,
#                         parse_mode=telegram.ParseMode.MARKDOWN)


# def stop_server(bot, update):
#     try:
#         i.stop()
#         bot.sendMessage(chat_id=update.message.chat_id,
#                         text='\xE2\x9D\x8C Выключение сервера.')
#     except Exception, e:
#         bot.sendMessage(chat_id=update.message.chat_id,
#                         text='\xF0\x9F\x98\xB5 *Скорее всего сервер выключен*. Вот ошибка: %s' % e,
#                         parse_mode=telegram.ParseMode.MARKDOWN)


def balance(bot, update):
    pass

def status(bot, update):
    if minecraft.Update().available:
        online = minecraft.Update().num_players_online

        def okonchanie(var):
            var = int(var)
            list_of_ok = [2, 3, 4]
            if var == 0:
                return 'пока никого нет'
            elif var in list_of_ok:
                return '%s человека' % var
            else:
                return '%s человек' % var

        bot.sendMessage(chat_id=update.message.chat_id,
                        text='\xE2\x9C\x85На сервере %s' % (okonchanie(int(online))),
                        parse_mode=telegram.ParseMode.MARKDOWN)

    else:
        bot.sendMessage(chat_id=update.message.chat_id,
                        text='\xE2\x9D\x8C Сервер Выключен.')


def unknown(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Неведомая команда... \xF0\x9F\x98\xB1")

# Bot init
updater = Updater(token=TELEGRAM_TOKEN)
job_queue = updater.job_queue
dispatcher = updater.dispatcher
dispatcher.addTelegramCommandHandler('start', start)
# dispatcher.addTelegramCommandHandler('run_server', run_server)
# dispatcher.addTelegramCommandHandler('stop_server', stop_server)
dispatcher.addTelegramCommandHandler('status', status)
dispatcher.addUnknownTelegramCommandHandler(unknown)
updater.start_polling()
updater.idle()
job_queue.stop()
