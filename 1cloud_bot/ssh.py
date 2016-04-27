# -*- coding: utf-8 -*-

from config import ADDRESS, START_SCRIPT, STOP_SCRIPT
import subprocess
import sys


# Ports are handled in ~/.ssh/config since we use OpenSSH
def run_command(cmd):
    ssh = subprocess.Popen(["ssh", "root@%s" % ADDRESS, cmd],
                           shell=False,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    result = ssh.stdout.readlines()
    if result == []:
        error = ssh.stderr.readlines()
        print >>sys.stderr, "ERROR: %s" % error
    else:
        print result


def start_minecraft():
    run_command('sh %s' % START_SCRIPT)


def stop_minecraft():
    run_command('sh %s' % STOP_SCRIPT)
