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
import sys
import time


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


def toggle_socket(target, action):
    socket = Energenie(int(target))
    logging.info("Turning '" + action + "' socket '" + str(target) + "'")
    if action == "on":
        socket.on()
    else:
        socket.off()


logging.info(script_name + " starting...")
logging.debug("script_dir..: '" + script_dir + "'")

# this is to avoid collisions when multiple commands are run at once...
timedelay = random.randrange(0, 45)
time.sleep(timedelay)

action = sys.argv[1].lower()
logging.info("Action......: '" + action + "'")
target = sys.argv[2].upper()
logging.info("Socket......: '" + target + "'")


if target == "ALL":
    for socket in range(1,5):
        toggle_socket(socket, action)
        time.sleep(1)
else:
    toggle_socket(target, action)


logging.info(script_name + " completed successfully.")
sys.exit(retcode)
