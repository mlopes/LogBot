#!/usr/bin/env python3

import signal
from logbot import Daemonizer
from logbot import IrcClient
from logbot import Logger

if __name__ == "__main__":
    logger = Logger()
    logger.initialise()

    irc_client = IrcClient('irc.freenode.net', 6667, '#openpassword', 'super_mega_bot', logger)
    irc_client.start()

    daemonizer = Daemonizer('/dev/null', '/tmp/daemon.log', '/tmp/daemon.log')
    daemonizer.add_signal_handler(signal.SIGTERM, irc_client.graceful_stop)
    daemonizer.daemonize(irc_client.process_forever)
