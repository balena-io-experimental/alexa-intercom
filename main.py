#!/usr/bin/python
import RPi.GPIO as GPIO
import time
from aiohttp import web
#import logging

#logging.basicConfig(format='%(levelname)s-%(asctime)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG,filename='/App/gpio.log')

# # Set GPIO mode: GPIO.BCM or GPIO.BOARD
# GPIO.setmode(GPIO.BOARD)
#
# # GPIO pins list based on GPIO.BOARD
# # gpioList1 = [3,5,7,8,10,11,12,13,15]
# # gpioList2 = [16,18,19,21,22,23,24,26]
#
# # Set mode for each gpio pin
# GPIO.setup(relay, GPIO.OUT)

# while True:
# 	# Change gpio pins from low to high
# 	GPIO.output(relay, 1)
# 	time.sleep(3)
# 	GPIO.output(relay, 0)
# 	time.sleep(0.5)
#
GPIO.setmode(GPIO.BOARD)
GPIO.setup(3, GPIO.OUT)
GPIO.output(3, 0)

def triggerRelay():
	relay = 3
	GPIO.output(relay, 1)
	time.sleep(3)
	GPIO.output(relay, 0)

async def opendoor(request):
	triggerRelay()
	return web.Response(content_type='text/html', text='ΟΚ')

if __name__ == '__main__':
	app = web.Application()
	app.router.add_get('/opendoor', opendoor)
	web.run_app(app, port=80)

# Reset all gpio pin
# GPIO.cleanup()
