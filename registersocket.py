#!/usr/bin/python
"""
Register an energenie socket.

Usage:
    registersocket.py <socket#> 

Example:
    registersocket.py 3

"""
#import the required modules
from energenie import switch_on, switch_off
import logging
import os
import random
import socket
import sys
import time


def toggle_socket(action, mysocket):
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

    mysocket = sys.argv[1]
    logging.debug("mysocket....: '" + mysocket + "'")


    if int(mysocket) > 0 and int(mysocket) < 5:
        raw_input("Hit return key to send socket '" + str(mysocket) + "' ON code.")
        toggle_socket('on', mysocket)
        raw_input("Hit return key to send socket '" + str(mysocket) + "' OFF code.")
        toggle_socket('off', mysocket)
    else:
        logging.info("Socket # must be between 1 and 4, not '" + str(mysocket) + "'.")
        sys.exit(2)


    logging.info(script_name + " completed successfully.")
    sys.exit(retcode)
