#!/usr/bin/python
"""
Control pimoroni targets.

This is reworked from pimoroni's example script.

Usage:
    lightcontrol.py <on|off> <socket#|ALL> 

Example:
    lightcontrol.py ON 1

"""
#import the required modules
from gpiozero import Energenie
import logging
import os
import random
import socket
import sys
import time


def toggle_socket(target, action):
    socket = Energenie(int(target))
    logging.info("Turning '" + action + "' socket '" + str(target) + "'")
    if action == "on":
        socket.on()
    else:
        socket.off()


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
    logging.debug("len.........: '" + str(len(sys.argv)) + "'")

    # reduce startup race conditions...
    timedelay = random.randrange(0, 3)
    time.sleep(timedelay)

    action = sys.argv[1].lower()
    logging.info("Action......: '" + action + "'")
    target = sys.argv[2].upper()
    logging.info("Socket......: '" + target + "'")

    get_lock(script_name)

    if target == "ALL":
        for socket in range(1,5):
            toggle_socket(socket, action)
            time.sleep(1)
    else:
        toggle_socket(target, action)

    logging.info(script_name + " completed successfully.")
    sys.exit(retcode)
