# -*- coding: utf-8 -*-

from config import SSH_USER, ADDRESS, START_SCRIPT, STOP_SCRIPT
import subprocess
import sys
import re


# Ports are handled in ~/.ssh/config since we use OpenSSH
def run_command(cmd):
    ssh = subprocess.Popen(["ssh", "%s@%s" % (SSH_USER, ADDRESS), cmd],
                           shell=False,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    result = ssh.stdout.readlines()
    if result == []:
        error = ssh.stderr.readlines()
        print >>sys.stderr, "ERROR: %s" % error
    else:
        return result


def start_minecraft():
    run_command('sh %s' % START_SCRIPT)


def stop_minecraft():
    run_command('sh %s' % STOP_SCRIPT)
