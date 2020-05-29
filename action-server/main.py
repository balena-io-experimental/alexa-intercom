#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import asyncio
from aiohttp import web
# from os import environ

relay = 3 # GPIO of relay
buzzer = 5 # GPIO of piezo
bell = False # state of auto bell feature
ringSense = 21 # GPIO of ring sense
counter = 0 # how many times the door has opened
# maxCounter = int(environ.get('MAX_COUNTER', '3')) # how many times to open the door per session (balenaCloud var)
maxCounter = 3

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(relay, GPIO.OUT)
GPIO.output(relay, 0)
GPIO.setup(buzzer, GPIO.OUT)
GPIO.output(buzzer, 0)
GPIO.setup(ringSense, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

async def triggerRelay(): # open the door
	GPIO.output(relay, 1)
	await asyncio.sleep(3)
	GPIO.output(relay, 0)

async def opendoor(request): # open the door
	asyncio.ensure_future(triggerRelay())
	return web.Response(content_type='text/html', text='The door is open')

async def bellon(request): # enable auto bell
	global bell
	global counter
	bell = True
	counter = 0
	return web.Response(content_type='text/html', text='Auto bell is enabled')

async def belloff(request): # disable auto bell
	global bell
	bell = False
	return web.Response(content_type='text/html', text='Auto bell is disabled')

async def getAutoBellState(request):
	global bell
	state = "Off"
	if bell:
		state = "On"
	return web.Response(content_type='text/html', text=state)

'''
async def autoBell(channel): # autoBell feature
	global bell
	global counter
	piezoTune() # play piezo tune
	if bell:
		counter += 1
		if counter <= maxCounter:
			asyncio.ensure_future(triggerRelay()) # open the door
		else:
			bell = False

GPIO.add_event_detect(ringSense, GPIO.RISING, callback=autoBell, bouncetime=500)
'''
def test(channel):
	print('button pressed!')

GPIO.add_event_detect(ringSense, GPIO.RISING, callback=test, bouncetime=500)

async def piezoTune(): # piezo tune
	GPIO.output(buzzer, 1)
	await asyncio.sleep(0.5)
	GPIO.output(buzzer, 0)
	await asyncio.sleep(0.5)
	GPIO.output(buzzer, 1)
	await asyncio.sleep(1)
	GPIO.output(buzzer, 0)

if __name__ == '__main__':
	app = web.Application()
	app.router.add_get('/opendoor', opendoor)
	app.router.add_get('/autobellon', bellon)
	app.router.add_get('/autobelloff', belloff)
	app.router.add_get('/autobellstate', getAutoBellState)
	web.run_app(app, port=80)
