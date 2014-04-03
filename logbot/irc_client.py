import irc.client
import sys
import time


class IrcClient(object):
    def __init__(self, server, port, channel, bot_name, logger, parser):
        self.server = server
        self.port = port
        self.channel = channel
        self.bot_name = bot_name
        self.logger = logger
        self.parser = parser
        self._client = None
        self._client_connection = None

    def start(self):
        self._client = irc.client.IRC()
        self._client_connection = self._client.server().connect(self.server, self.port, self.bot_name)
        self._add_handlers()

    def _add_handlers(self):
        self._client_connection.add_global_handler('pubmsg', self.log)
        self._client_connection.add_global_handler('privmsg', self.answer)
        self._client_connection.add_global_handler('welcome', self.joinner)

    def joinner(self, connection, event):
        connection.join(self.channel)

    def log(self, connection, event):
        self.logger.write(event.source.nick, event.arguments[0])

    def answer(self, connection, event):
        for msg in self.parser.parse(event.arguments[0]):
            connection.privmsg(event.source.nick, msg)
            time.sleep(1)

    def graceful_stop(self, signum, frame):
        self._client.disconnect_all("{0} is going home now.".format(self.bot_name))
        self.logger.close()
        sys.exit(0)

    def process_forever(self):
        self._client.process_forever()
