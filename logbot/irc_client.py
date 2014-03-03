import irc.client
import sys
import os


class IrcClient(object):
    def __init__(self, server, port, channel, bot_name):
        self.server = server
        self.port = port
        self.channel = channel
        self.bot_name = bot_name

    def start(self):
        self._client = irc.client.IRC()
        self._client_connection = self._client.server().connect(self.server, self.port, self.bot_name)
        self._add_handlers()

    def _add_handlers(self):
        self._client_connection.add_global_handler('pubmsg', self.logger)
        self._client_connection.add_global_handler('welcome', self.joinner)

    def joinner(self, connection, event):
        connection.join(self.channel)

    def logger(self, connection, event):
        sys.stdout.write(event.arguments[0])
        sys.stdout.flush()

    def graceful_stop(self, signum, frame):
        self._client.disconnect_all("{0} is going home now.".format(self.bot_name))
        os._exit(0)

    def process_forever(self):
        self._client.process_forever()
