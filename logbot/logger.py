import sqlite3


class Logger(object):
    _table_name = 'irc_log'
    _database_name = "logbot.db"

    def initialise(self):
        self.connection = sqlite3.connect(self._database_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS {0} (nick, message, timestamp)".format(self._table_name))

    def write(self, nick, message):
        self.cursor.execute("INSERT INTO {0} VALUES (?, ?, DATETIME('NOW'))".format(self._table_name), (nick, message))
        self.connection.commit()

    def last(self, limit):
        self.cursor.execute(
            "SELECT nick, message, timestamp FROM {0} order by timestamp DESC LIMIT ?".format(self._table_name),
            (limit, ))

        last_messages = self.cursor.fetchall()
        last_messages.reverse()
        return last_messages

    def close(self):
        self.connection.close()
