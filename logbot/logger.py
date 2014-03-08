import sqlite3
import sys

class Logger(object):
    _table_name = 'irc_log'
    _database_name = "logbot.db"

    def __init__(self):
        self.connection = None
        self.cursor = None

    def initialise(self):
        self.connection = sqlite3.connect(self._database_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS {0} (nick, message, timestamp)".format(self._table_name))

    def write(self, nick, message):
        self.cursor.execute("INSERT INTO {0} VALUES (?, ?, DATETIME('NOW'))".format(self._table_name), (nick, message))
        self.connection.commit()

    def last(self, limit):
        self.cursor.execute(
            self._select(order_by = "ORDER BY timestamp DESC", limit = "LIMIT ?"),
            (limit, ))

        last_messages = self.cursor.fetchall()
        last_messages.reverse()
        return last_messages

    def find(self, search_string):
        self.cursor.execute(
            self._select(
                where = "WHERE message like '%{0}%'".format(search_string),
                order_by = "ORDER BY timestamp ASC"
            )
        )

        return tuple(self.cursor.fetchall())

    def date(self, search_date):
        self.cursor.execute(
            self._select(
                where = "WHERE timestamp between '{0} 00:00:00' AND '{0} 23:59:59'".format(search_date),
                order_by = "ORDER BY timestamp ASC"
            )
        )
        return tuple(self.cursor.fetchall())

    def _select(self, where = '', order_by = '', limit = ''):
        sys.stdout.write("SELECT nick, message, timestamp FROM {0} {1} {2} {3}".format(self._table_name, where, order_by, limit))
        return "SELECT nick, message, timestamp FROM {0} {1} {2} {3}".format(self._table_name, where, order_by, limit)

    def close(self):
        self.connection.close()
