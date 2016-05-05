# -*- coding: utf-8 -*-

import requests
from config import HOSTING_API, SERVER_ID
import json

AUTH = {'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % HOSTING_API}


def response(r):
    if r.status_code == 200:
        return r.json()
    else:
        return 'Код ошибки: %s. Сообщение: %s' % (r.status_code, r.content)


def get_balance():
    dest = 'https://api.1cloud.ru/customer/balance'
    r = requests.get(dest, headers=AUTH)
    return response(r)


def server_status():
    dest = 'https://api.1cloud.ru/server/%s' % SERVER_ID
    r = requests.get(dest, headers=AUTH)
    return response(r)


# Action: PowerOn, PowerOff, PowerReboot
def action_with(action):
    dest = 'https://api.1cloud.ru/Server/%s/Action' % SERVER_ID
    body = {'Type': action}
    r = requests.post(dest, headers=AUTH, data=json.dumps(body))
    return response(r)

# DEPRECATED
# def is_server_power_on():
#     if server_status()['IsPowerOn'] == True:
#         return True
#     else:
#         return False
