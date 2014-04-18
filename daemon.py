#!/usr/bin/python
import sys, os, urllib2

''' Module to fork the current process as a daemon.
    Note: don't do any of this if your daemon get started by inetd!
    inetd does all you need, icluding redirecting standard file descriptors;
    the chdir() and umask() steps are the only ones you may still want.
'''

def daemonize (stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
    ''' Fork the current process as a daemon, redirecting standard file
        descriptors (by default, redirects them to /dev/null).
    '''

    # Perform first fork.
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0) # Exit first parent.
    except OSError, e:
        sys.stderr.write("fork #1 failed: (%d) %s\n" % (e.errno, e.strerror))
        sys.exit(1)

    # Decouple from parent environment.
    os.chdir("/")
    os.umask(0)
    os.setsid()

    # Perform second fork.
    try:
        pid = os.fork();
        if pid > 0:
            sys.exit() # Exit second parent.
    except OSError, e:
        sys.stderr.write("fork #2 failed: (%d) %s\n" % (e.errno, e.strerror))
        sys.exit(1)

    # The process is now daemonized, redirect standard file descriptors.
    for f in sys.stdout, sys.stderr: f.flush()
    si = file(stdin, 'r')
    so = file(stdout, 'a+')
    se = file(stderr, 'a+', 0)
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())

def _app_main ():
    ''' Example main function: print a count & timestamp each second '''

    import time
    sys.stdout.write('Daemon started with pid %d\n' % os.getpid())
    sys.stdout.write('Daemon stdout output\n')
    sys.stderr.write('Daemon stderr output\n')
    c = 0
    while True:
        sys.stdout.write('%d: %s\n' % (c, time.ctime()))
        sys.stdout.flush()
        c = c + 1
        time.sleep(1)
        print urllib2.urlopen('http://kick.cncore.com/test.php?arg1=1&arg2=2').read()

if __name__ == "__main__":
    daemonize('/dev/null','/tmp/daemon.log','/tmp/daemon.log')
    _app_main()
