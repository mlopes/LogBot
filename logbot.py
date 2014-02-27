import os
import time
import signal


def daemonize(workingdir='.', umask=0, outfile='/dev/null'):
# Put in background
    pid = os.fork()
    if pid == 0:
        # First child
        os.setsid()
        pid = os.fork()  # fork again
        if pid == 0:
            os.chdir(workingdir)
            os.umask(umask)
        else:
            os._exit(0)
    else:
        os._exit(0)

    # Close all open resources
    try:
        os.close(0)
        os.close(1)
        os.close(2)
    except:
        raise Exception("Unable to close standard output. Try running with 'nodaemon'")
        os._exit(1)

    #Redirect output
    os.open(outfile, os.O_RDWR | os.O_CREAT)
    os.dup2(0, 1)
    os.dup2(0, 2)

    signal.signal(signal.SIGTERM, handler)

    while 1:
        print("whiling")
        time.sleep(5)


def handler(signum, frame):
    print("exiting cleanly")
    os._exit(0)

daemonize(".", 0, "logfile")
