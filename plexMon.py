#!/usr/bin/env python
import urllib2
import xml.etree.ElementTree as ET
from os.path import expanduser
import logging
import logging.handlers
import httplib
import urllib

ignoreAlertList = []  # Add any myPlex usernames to this list (like your own) to disable alerting for them. Will still be logged.

def sendAlert(alertText):

  conn = httplib.HTTPSConnection("api.pushover.net:443")
  conn.request("POST", "/1/messages.json",
    urllib.urlencode({
      "token": "PUSHOVER_TOKEN",  # Replace with your Pushover Application Token
      "user": "PUSHOVER_USERID",  # Replace with your Pushover User ID
      "title": 'plexMon',
      "message": alertText,
      "sound": "intermission",
    }), {"Content-type": "application/x-www-form-urlencoded"})
  conn.getresponse()

logLocation = expanduser('~') + '/Library/Logs/plexMon.log'  # Log location is Mac OS X specfic, update if on a different platform
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', filename=logLocation, level=logging.INFO)
log = open(logLocation).read()

server = urllib2.urlopen('http://IP:PORT/status/sessions')  # Replace the IP and Port with those of your server
data = server.read()
server.close()
tree = ET.fromstring(data)
for video in tree.iter('Video'):
  title = '%s - %s' % (video.get('grandparentTitle'), video.get('title'))
  user = video.find('User').get('title').split('@')[0]
  alert = '%s is watching %s' % (user, title)
  if alert not in log:
    logging.info(alert)
    if all(i not in alert for i in ignoreAlertList):
      sendAlert(alert)
