import os
import sys
import signal
import irc.client


def daemonize(stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)  # Exit first parent.
    except OSError as e:
        sys.stderr.write("fork #1 failed: (%d) %s\n" % (e.errno, e.strerror))
        sys.exit(1)

    # Decouple from parent environment.
    os.chdir("/")
    os.umask(0)
    os.setsid()

    # Do second fork.
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)  # Exit second parent.
    except OSError as e:
        sys.stderr.write("fork #2 failed: (%d) %s\n" % (e.errno, e.strerror))
        sys.exit(1)

    # Now I am a daemon!

    # Redirect standard file descriptors.
    si = open(stdin, 'r')
    so = open(stdout, 'a+')
    se = open(stderr, 'a+')
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())

    signal.signal(signal.SIGTERM, handler)


def handler(signum, frame):
    if signum == signal.SIGTERM:
        print("exiting cleanly")
        os._exit(0)


def main():
    sys.stdout.write('Daemon started with pid %d\n' % os.getpid())
    sys.stdout.write('Daemon stdout output\n')
    sys.stderr.write('Daemon stderr output\n')
    irciffy()


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
    daemonize('/dev/null', '/tmp/daemon.log', '/tmp/daemon.log')
    main()
