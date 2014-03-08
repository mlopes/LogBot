import re


class ContextNotFound(Exception):
    pass


class Parser(object):

    _commands = ('help', 'last', 'find', 'date')

    def __init__(self, logger):
        self.logger = logger
        self._default_limit = 50
        self.message = None

    def parse(self, message):
        for command in self._commands:
            if message.startswith(command):
                handler = self.__getattribute__('_' + command)
                self.message = message
                return handler()
        return ("That sounds interesting! It's not like I'm falling asleep or anything like that mate.", )

    def _help(self):
        self.message = None
        return (
            "help - shows these help",
            "last n - shows the last n messages on the channel",
            "find word - shows latest messages containing word",
            "date yyyy-mm-dd - show messages from date"
        )

    def _last(self):
        search_result = re.search('\d+', self.message)
        try:
            limit = int(search_result.group(0))
        except AttributeError:
            limit = self._default_limit
        except ValueError:
            limit = self._default_limit

        self.message = None
        return self.logger.last(limit)

    def _find(self):
        try:
            to_find = self._extract_context()
        except ContextNotFound:
            return ("Sorry, couldn't quite understand what you're trying to find", )

        self.message = None
        return self.logger.find(to_find)

    def _extract_context(self):
        try:
            context = self.message.partition(' ')[2]
        except:
            self.message = None
            raise ContextNotFound
        return context

    def _date(self):
        try:
            date_context = self._extract_context()
        except ContextNotFound:
            return ("Sorry, couldn't quite understand which date you're looking for", )

        date_search = re.search('\d\d\d\d-\d\d-\d\d', date_context)
        try:
            date = date_search.group(0)
        except AttributeError:
            return ("Sorry, couldn't quite understand which date you're looking for", )

        return self.logger.date(date)
