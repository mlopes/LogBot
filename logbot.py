#!/usr/bin/env python3

import os
import sys
import signal
import irc.client
from logbot import Daemonizer


def handler(signum, frame):
    if signum == signal.SIGTERM:
        print("exiting cleanly")
        os._exit(0)


def f(c, e):
    sys.stdout.write(e.arguments[0])
    sys.stdout.flush()


def irciffy():
    client = irc.client.IRC()
    c = client.server().connect('irc.freenode.net', 6667, 'op_bot')
    c.join("#openpassword")
    c.add_global_handler('pubmsg', f)
    c.add_global_handler('privmsg', f)

    client.process_forever()


if __name__ == "__main__":
    daemonizer = Daemonizer('/dev/null', '/tmp/daemon.log', '/tmp/daemon.log')
    daemonizer.add_signal_handler(signal.SIGTERM, handler)
    daemonizer.daemonize(irciffy)
