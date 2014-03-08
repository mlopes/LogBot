#!/usr/bin/env python3

import signal
from logbot import Daemonizer
from logbot import IrcClient
from logbot import Logger
from logbot import Parser

if __name__ == "__main__":
    logger = Logger()
    logger.initialise()

    parser = Parser(logger)

    irc_client = IrcClient('your.favourite.irc.server', 6667, '#yourfavouritechannel', 'super_mega_bot', logger, parser)
    irc_client.start()

    daemonizer = Daemonizer('/dev/null', '/tmp/daemon.log', '/tmp/daemon.log')
    daemonizer.add_signal_handler(signal.SIGTERM, irc_client.graceful_stop)
    daemonizer.daemonize(irc_client.process_forever)
