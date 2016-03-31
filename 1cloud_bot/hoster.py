# -*- coding: utf-8 -*-

import requests
from config import HOSTING_API, SERVER_ID
import json

AUTH = {'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % HOSTING_API}


def get_balance():
    dest = 'https://api.1cloud.ru/customer/balance'
    r = requests.get(dest, headers=AUTH)
    if r.status_code == 200:
        return r.content
    else:
        return 'Код ошибки: %s. Сообщение: %s' % (r.status_code, r.content)


def server_status():
    dest = 'https://api.1cloud.ru/server/%s' % SERVER_ID
    r = requests.get(dest, headers=AUTH)
    if r.status_code == 200:
        return r.json()
    else:
        return 'Код ошибки: %s. Сообщение: %s' % (r.status_code, r.content)


# Action: PowerOn, PowerOff, PowerReboot
def action_with(action):
    dest = 'https://api.1cloud.ru/Server/%s/Action' % SERVER_ID
    body = {'Type': action}
    r = requests.post(dest, headers=AUTH, data=json.dumps(body))
    if r.status_code == 200:
        return r.json()
    else:
        return 'Код ошибки: %s. Сообщение: %s' % (r.status_code, r.content)
