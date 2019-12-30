#!/usr/bin/python
"""
Register energenie sockets for control.

Usage:
    registersocket.py <socket#> 

Example:
    registersocket.py 1

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


if __name__ == "__main__":

    if len(sys.argv) < 2:
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

    target = int(sys.argv[1])
    logging.info("Socket......: '" + str(target) + "'")

    if target >= 1 and target <= 4:
        raw_input("Hit return key to send socket '" + str(target) + "' ON code.")
        toggle_socket(target, 'on')
        raw_input("Hit return key to send socket '" + str(target) + "' OFF code.")
        toggle_socket(target, 'off')
    else:
        logging.info("Socket # must be between 1 and 4, not '" + str(target) + "'.")
        sys.exit(2)

    logging.info(script_name + " completed successfully.")
    sys.exit(retcode)
