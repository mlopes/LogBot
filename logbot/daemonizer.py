import os
import sys
import signal


class Daemonizer(object):
    def __init__(self, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self._fork_count = 0
        self.signal_handler = {}
        self.base_path = "/"

    def daemonize(self, runner):
        self._fork()
        self._decouple()
        self._fork()
        self._redirect_standard_file_descriptors()
        self._add_signal_handlers()
        runner()

    def _fork(self):
        self._fork_count += 1
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)  # Exit parent.
        except OSError as e:
            sys.stderr.write("fork #(%d) failed: (%d) %s\n" % (self._fork_count, e.errno, e.strerror))
            sys.exit(1)

    # noinspection PyArgumentList
    def _decouple(self):
        os.chdir(self.base_path)
        os.umask(0)
        os.setsid()

    def _redirect_standard_file_descriptors(self):
        si = open(self.stdin, 'r')
        so = open(self.stdout, 'a+')
        open(self.stderr, 'a+')
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())

    def _add_signal_handlers(self):
        for each_signal in self.signal_handler:
            signal.signal(each_signal, self.signal_handler[each_signal])

    def add_signal_handler(self, signal_number, handler):
        self.signal_handler[signal_number] = handler
