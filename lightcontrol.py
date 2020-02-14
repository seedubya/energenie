#!/usr/bin/python
"""
Control pimoroni targets.

This is reworked from pimoroni's example script. This will take several sockets
as arguments...

Light control:
    lightcontrol.py <on|off> <socket#|ALL> 

Example:
    lightcontrol.py ON 1 2 3    - turn ON sockets 1, 2 & 3

Socket registration:
    lightcontrol.py reg <socket #>

Example:
    lightcontrol.py reg 3    - register socket 3

"""
#import the required modules
from energenie import switch_on, switch_off
import logging
import os
import random
import socket
import sys
import time


def get_lock(process_name):
    # Without holding a reference to our socket somewhere it gets garbage
    # collected when the function exits
    get_lock._lock_socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)

    while True:
        try:
            get_lock._lock_socket.bind('\0' + process_name)
            # we have the lock...
        except:
            logging.info("I'm already running, sleeping for a bit...")
            timedelay = random.randrange(0, 10)
            time.sleep(timedelay)
            continue
        break

def toggle_socket(action, mysocket):
    # do the actual switching here...
    if mysocket == 'ALL':
        if action == "ON":
            logging.info("Turning ALL on...")
            switch_on()
        else:
            logging.info("Turning ALL off...")
            switch_off()
    else:
        if int(mysocket) > 0 and int(mysocket) < 5:
            if action == "ON":
                logging.info("Turning socket '" + mysocket + "' on...")
                switch_on(int(mysocket))
            else:
                logging.info("Turning socket '" + mysocket + "' off...")
                switch_off(int(mysocket))
            time.sleep(1)
        else:
            logging.debug("Skipping out of range socket.")


if __name__ == "__main__":

    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)


    script_name = os.path.basename(__file__)
    script_dir = os.path.dirname(__file__)
    retcode = 0


    if os.getenv("DEBUG", "") == "":
        logging.basicConfig(format='%(asctime)s %(levelname)-10s: %(message)s', level=logging.INFO)
    else:
        logging.basicConfig(format='%(asctime)s %(levelname)-10s: %(message)s', level=logging.DEBUG)


    logging.info(script_name + " starting...")
    logging.debug("script_dir..: '" + script_dir + "'")

    # reduce startup race conditions...
    timedelay = random.randrange(0, 3)
    time.sleep(timedelay)

    action = sys.argv[1].upper()
    logging.debug("Action......: '" + action + "'")

    get_lock(script_name)

    if action == 'REG':
        # register a new socket - we only do 1 at a time...
        mysocket = sys.argv[2]
        try:
            myjunk = int(mysocket)
            if int(mysocket) > 0 and int(mysocket) < 5 :
                raw_input("Hit return key to send socket '" + mysocket + "' ON code.")
                toggle_socket('on', mysocket)
                raw_input("Hit return key to send socket '" + mysocket + "' OFF code.")
                toggle_socket('off', mysocket)
                logging.info("Socket registered.")
            else:
                logging.info("Socket # must be between 1 and 4, not '" + mysocket + "'.")
                sys.exit(2)
        except ValueError:
            logging.info("Should be a socket number 1<=x<=4, not '" + mysocket + "'.")
            sys.exit(3)
    else:
        # Turn sockets on or off...
        for myvar in range(2,len(sys.argv)):
            mysocket = sys.argv[myvar].upper()
            logging.debug("mysocket....: '" + mysocket + "'")
            toggle_socket(action, mysocket)

    logging.info(script_name + " completed successfully.")
    sys.exit(retcode)
