import sqlite3


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
            self._select(order_by="ORDER BY timestamp DESC", limit="LIMIT ?"),
            (limit, ))

        last_messages = self.cursor.fetchall()
        last_messages.reverse()
        return last_messages

    def find(self, search_string):
        self.cursor.execute(
            self._select(
                where="WHERE message like ?",
                order_by="ORDER BY timestamp ASC"
            ),
            ("%{0}%".format(search_string), )
        )

        return tuple(self.cursor.fetchall())

    def date(self, search_date):
        self.cursor.execute(
            self._select(
                where="WHERE timestamp between ? AND ?",
                order_by="ORDER BY timestamp ASC"
            ),
            ("{0} 00:00:00".format(search_date), "{0} 23:59:59".format(search_date))
        )
        return tuple(self.cursor.fetchall())

    def _select(self, where='', order_by='', limit=''):
        return "SELECT nick, message, timestamp FROM {0} {1} {2} {3}".format(self._table_name, where, order_by, limit)

    def close(self):
        self.connection.close()
