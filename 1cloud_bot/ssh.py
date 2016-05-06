# -*- coding: utf-8 -*-
from config import SSH_USER, ADDRESS, START_SCRIPT, STOP_SCRIPT, PATH_TO_MINECRAFT_LOG
import subprocess
import re
import os


# Ports are handled in ~/.ssh/config since we use OpenSSH
def _run_command(cmd):
    ssh = subprocess.Popen(["ssh", "%s@%s" % (SSH_USER, ADDRESS), cmd],
                           shell=False,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    result = ssh.stdout.readlines()
    if result == []:
        error = ssh.stderr.readlines()
        return "ERROR: %s" % error
    else:
        return result


def is_server_on():
    response = os.system("ping -c 1 %s >/dev/null" % ADDRESS)
    if response == 0:
        return True
    else:
        return False


def free_mem():
    raw = _run_command('cat /proc/meminfo | grep -i "MemFree"')
    result = re.findall(r'\d+', raw[0])[0]
    return result  # Return result in KB


def cpu_load():
    raw = _run_command('cat /proc/loadavg')
    result = raw[0].split()[:-2]
    return result


def swap():
    swap_total = _run_command('cat /proc/meminfo | grep -i "SwapTotal"')
    swap_total = re.findall(r'\d+', swap_total[0])[0]

    swap_free = _run_command('cat /proc/meminfo | grep -i "SwapFree"')
    swap_free = re.findall(r'\d+', swap_free[0])[0]

    return int(swap_total) - int(swap_free)


def reboot_cmd():
    _run_command('reboot')


def shutdown_cmd():
    _run_command('shutdown -h now')


def start_minecraft():
    return _run_command('sh %s' % START_SCRIPT)


def stop_minecraft():
    return _run_command('sh %s' % STOP_SCRIPT)


def _remove_trash_info_from_log(input_list):
    formatted_list = []
    junk = ['[', ']', 'Server thread/', 'chunks for level ', 'INFO: ']
    for line in input_list:
        formatted_string = line
        for i in junk:
            formatted_string = formatted_string.replace(i, '')
        formatted_list.append(formatted_string)
    return formatted_list


def get_log(tail=False):
    raw = _run_command('cat %s' % PATH_TO_MINECRAFT_LOG)
    pretty_log = _remove_trash_info_from_log(raw)
    if tail:
        tail_lines = -10
        return ''.join(pretty_log[tail_lines:])
    else:
        return ''.join(pretty_log)
