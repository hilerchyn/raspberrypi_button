#!/usr/bin/python
import sys, os, urllib2, time
import RPi.GPIO as GPIO

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

if __name__ == "__main__":
    daemonize('/dev/null','/dev/null','/dev/null')

    button_pin_23 = 23
    button_pin_24 = 24
    
    pin_23_counter = 0
    pin_24_counter =0

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(button_pin_23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(button_pin_24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
    sys.stdout.write('Daemon started with pid %d\n' % os.getpid())
    sys.stdout.write('Daemon stdout output\n')
    sys.stderr.write('Daemon stderr output\n')
    c = 0
    
    while True:
        
        if (GPIO.input(button_pin_23)):
            time.sleep(2)
            if(pin_23_counter==0):
                pin_23_counter=1
                try:
                    print urllib2.urlopen('http://192.168.1.189:8080/led/sys/ledAction_point1.action').read()
                except urllib2.URLError, e:
                    print "23 connection failed"
        elif (GPIO.input(button_pin_24)):
            time.sleep(2)
            if(pin_24_counter==0):
                pin_24_counter=1
                try:
                    print urllib2.urlopen('http://192.168.1.189:8080/led/sys/ledAction_point2.action').read()
                except urllib2.URLError, e:
                    print "24 connection failed"
        else:
            if(pin_23_counter > 0):
                pin_23_counter =0
                
            if(pin_24_counter > 0):
                pin_24_counter =0
                
