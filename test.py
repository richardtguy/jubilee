#!/usr/local/bin/python3

import time
from jubilee import ibeacon, lights
import sys, logging
import config
import soco

# set up logging
logger = logging.getLogger(__name__)
logging_level = sys.argv[1].upper()
logging.basicConfig(
	filename='test.log',
	level=logging_level,
	format='%(asctime)-12s | %(levelname)-8s | %(name)s | %(message)s',
	datefmt='%d/%m/%y, %H:%M:%S'
)


# Test bridge (Hue and Lightify)
"""
bridge = lights.Bridge(hue_uname=config.HUE_USERNAME, hue_IP=config.HUE_IP_ADDRESS, lightify_IP=config.LIGHTIFY_IP)

for light in bridge:
	light.off()
	
time.sleep(2)

for light in bridge:
	light.on()
"""


# Test presence sensor
def welcome_home(person):
	print('welcome home %s' % (person))
	
def bye(person):
	print('bye')

presence_sensor = ibeacon.PresenceSensor(welcome_callback=welcome_home, last_one_out_callback=bye, topic='ibeacon/fqko3', scan_timeout=config.SCAN_TIMEOUT)
beacon1 = {"UUID": "FDA50693-A4E2-4FB1-AFCF-C6EB07647825", "Major": "10004", "Minor": "54480"}
beacon2 = {"UUID": "FDA50693-A4E2-4FB1-AFCF-C6EB07647825", "Major": "10004", "Minor": "54481"}
print((presence_sensor.register_beacon(beacon1, "Richard")))
print((presence_sensor.register_beacon(beacon2, "Michelle")))
presence_sensor.start()

time.sleep(10)

presence_sensor.stop()


# Test remote control
bridge = None

remote = lights.Remote(config.MQTT_HOST, config.MQTT_PORT, config.MQTT_UNAME, config.MQTT_PWORD, bridge)
remote.start()
time.sleep(60)
remote.stop()


# test discovery and control of Sonos speakers
print('Connecting to Sonos speakers...', end='')
speakers = soco.discover()
if speakers != None:
	for speaker in speakers:
		logger.info('Discovered speaker: %s' % (speaker.player_name))
	print(' OK')
else:
	print(' No speakers found')

if speakers != None:
	logger.info("Turning speakers off...")
	for speaker in speakers:
		speaker.play()

time.sleep(5)

if speakers != None:
	logger.info("Turning speakers off...")
	for speaker in speakers:
		speaker.stop()



