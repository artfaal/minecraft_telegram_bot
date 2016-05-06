# -*- coding: utf-8 -*-
from config import SSH_USER, ADDRESS, START_SCRIPT, STOP_SCRIPT, PATH_TO_MINECRAFT_LOG
import subprocess
import re
import os


# Ports are handled in ~/.ssh/config since we use OpenSSH
def run_command(cmd):
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


def start_minecraft():
    return run_command('sh %s' % START_SCRIPT)


def stop_minecraft():
    return run_command('sh %s' % STOP_SCRIPT)
def is_server_on():
    response = os.system("ping -c 1 -t 3 %s >/dev/null" % ADDRESS)
    if response == 0:
        return True
    else:
        return False


def free_mem():
    raw = run_command('cat /proc/meminfo | grep -i "MemFree"')
    result = re.findall(r'\d+', raw[0])[0]
    return result  # Return result in KB


def cpu_load():
    raw = run_command('cat /proc/loadavg')
    result = raw[0].split()[:-2]
    return result


def swap():
    swap_total = run_command('cat /proc/meminfo | grep -i "SwapTotal"')
    swap_total = re.findall(r'\d+', swap_total[0])[0]

    swap_free = run_command('cat /proc/meminfo | grep -i "SwapFree"')
    swap_free = re.findall(r'\d+', swap_free[0])[0]

    return int(swap_total) - int(swap_free)


def reboot_cmd():
    run_command('reboot')


def shutdown_cmd():
    run_command('shutdown -h now')


def get_log():
    raw = run_command('cat %s' % PATH_TO_MINECRAFT_LOG)
    return ''.join(raw)


def is_server_on():
    response = os.system("ping -c 1 %s >/dev/null" % ADDRESS)
    if response == 0:
        return True
    else:
        return False
