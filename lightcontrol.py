#!/usr/bin/python
"""
Control pimoroni targets.

This is reworked from pimoroni's example script.

Usage:
    lightcontrol.py <socket#|ALL> <on|off>

Example:
    lightcontrol.py 1 OFF

"""
#import the required modules
import RPi.GPIO as GPIO
import logging
import os
import sys
import time


if len(sys.argv) < 2:
    print(__doc__)
    sys.exit(1)


script_name = os.path.basename(__file__)
script_dir = os.path.dirname(__file__)
retcode = 0

# these are the socket addresses...
sockall="011"	# all sockets...
sock1="111"
sock2="110"
sock3="101"
sock4="100"

if os.getenv("DEBUG", "") == "":
    logging.basicConfig(format='%(asctime)s %(levelname)-10s: %(message)s', level=logging.INFO)
else:
    logging.basicConfig(format='%(asctime)s %(levelname)-10s: %(message)s', level=logging.DEBUG)


def init_gpio():
    # set the pins numbering mode
    GPIO.setmode(GPIO.BOARD)

    # Select the GPIO pins used for the encoder K0-K3 data inputs
    GPIO.setup(11, GPIO.OUT)
    GPIO.setup(15, GPIO.OUT)
    GPIO.setup(16, GPIO.OUT)
    GPIO.setup(13, GPIO.OUT)

    # Select the signal used to select ASK/FSK
    GPIO.setup(18, GPIO.OUT)

    # Select the signal used to enable/disable the modulator
    GPIO.setup(22, GPIO.OUT)

    # Disable the modulator by setting CE pin lo
    GPIO.output (22, False)

    # Set the modulator to ASK for On Off Keying
    # by setting MODSEL pin lo
    GPIO.output (18, False)

    # Initialise K0-K3 inputs of the encoder to 0000
    GPIO.output (11, False)
    GPIO.output (15, False)
    GPIO.output (16, False)
    GPIO.output (13, False)


def toggle_sockets(actionstring):
    gpio_pins = "13 16 15 11"

    mydict = {}
    mydict = dict(zip(gpio_pins.split(), list(actionstring)))

    for k,v in mydict.items():
        logging.debug("key.........: '" + k + "' value '" + str(v) + "'")
        if v == '0':
            logging.debug("Setting FALSE")
	    GPIO.output (int(k), False)
        else:
            logging.debug("Setting TRUE")
	    GPIO.output (int(k), True)
    
    # let it settle, encoder requires this
    time.sleep(0.1)

    # Enable the modulator
    GPIO.output (22, True)

    # keep enabled for a period
    time.sleep(0.25)

    # Disable the modulator
    GPIO.output (22, False)


logging.info(script_name + " starting...")
logging.debug("script_dir..: '" + script_dir + "'")

init_gpio()

target = sys.argv[1].upper()
logging.info("Socket......: '" + target + "'")
action = sys.argv[2].upper()
logging.info("Action......: '" + action + "'")

actionstring = ""
if action == 'ON':
    actionstring = "1"
else:
    actionstring = "0"

if target == "1":
    logging.debug("Socket 1")
    actionstring = actionstring + sock1
elif target == "2":
    logging.debug("Socket 2")
    actionstring = actionstring + sock2
elif target == "3":
    logging.debug("Socket 3")
    actionstring = actionstring + sock3
elif target == "4":
    logging.debug("Socket 4")
    actionstring = actionstring + sock4
else:
    logging.debug("All sockets.")
    actionstring = actionstring + sockall
    
logging.debug("actionstring: '" + actionstring + "'")

toggle_sockets(actionstring)

GPIO.cleanup()

logging.info(script_name + " completed successfully..")
sys.exit(retcode)
