# -*- coding: utf-8 -*-

import traceback
import string
import datetime
import os
import sys
import logging
import json
import urllib

from smarter.SmarterInterface import *
from smarter.SmarterProtocol import *

#------------------------------------------------------
# iBrew:
#
# Python protocol interface to Smarter Appliances
#
# https://github.com/Tristan79/iBrew
#
# Copyright © 2017 Tristan (@monkeycat.nl). All Rights Reserved
#
# The Dream Tea
#------------------------------------------------------


url_mass = 'http://%s/json.htm?type=command&param=udevice&hid=%s&' \
              'did=%s&dunit=%s&dtype=93&dsubtype=1&nvalue=0&svalue=%s'
url_per = 'http://%s/json.htm?type=command&param=udevice&idx=%s&nvalue=0&svalue=%s'
url_hardware_add = 'http://%s/json.htm?type=command&param=addhardware&htype=15&port=1&name=%s&enabled=true'
url_hardware = 'http://%s/json.htm?type=hardware'
url_sensor = 'http://%s/json.htm?type=devices&filter=utility&order=Name'
url_sensor_add = 'http://%s/json.htm?type=createvirtualsensor&idx=%s&sensorname=%s&sensortype=%s'
url_sensor_ren = 'http://%s/json.htm?type=command&param=renamedevice&idx=%s&name=%s'
url_trigger_value = 'http://%s/json.htm?type=command&param=udevice&idx=%s&nvalue=0&svalue=§N'
url_trigger_switch = 'http://%s/json.htm?type=command&param=switchlight&idx=%s&switchcmd=§N'
url_trigger_user = 'http://%s/json.htm?type=command&param=updateuservariable&vname=%s&vtype=0&vvalue=§N'

class iBrewDomoticz:


    def open_url(self,url):
        logging.debug('iBrew: Domoticz: Opening url: %s' % (url))
        try:
            response = urllib.urlopen(url)
        except Exception, e:
            logging.error('iBrew: Domoticz: Failed to send data to Domoticz (%s)' % (url))
            return 'None'
        return response


    def exists_hardware(self,name):
        response = self.open_url(url_hardware % (self.domoticzurl))
        if response == 'None':
            return 'None'
        data = json.loads(response.read())
        if 'result' in data:
            for i in range(0,len(data['result'])):
                if name == data['result'][i]['Name']:
                    return data['result'][i]['idx']
        return 'None'

    # Check if hardware exists and add if not..

    def __init__(self,connection="127.0.0.1:8080",name="iBrew"):
        self.domoticzurl = connection
        self.hardwarename = name
    
    def check_hardware(self):
        self.hardwareid = self.exists_hardware(self.hardwarename)
        if 'None' == self.hardwareid:
            response = self.open_url(url_hardware_add % (self.domoticzurl, self.hardwarename.replace(' ', '%20')))
            self.hardwareid = self.exists_hardware(self.hardwarename)
            if 'None' == self.hardwareid:
                    logging.error('iBrew: Domoticz: Unable to access Domoticz hardware')
                    return False
        return True

    def exists_sensor(self,name):
        self.query
        self.data
        if self.query:
            response = self.open_url(url_sensor % (self.domoticzurl))
            self.data = json.loads(response.read())
            self.query = False
        if 'result' in self.data:
            for i in range(0,len(data['result'])):
                if name == self.data['result'][i]['Name'] and int(self.hardwareid) == self.data['result'][i]['HardwareID']:
                    return self.data['result'][i]['idx']
        return 'None'

    def exists_id(sensorid):
        self.query
        self.data
        if self.query:
            response = self.open_url(url_sensor % (self.domoticzurl))
            self.data = json.loads(response.read())
            self.query = False
        if 'result' in self.data:
            for i in range(0,len(self.data['result'])):
                if sensorid == self.data['result'][i]['idx'] and int(self.hardwareid) == self.data['result'][i]['HardwareID']:
                    return True
        return False

    def setup(self,client,connection,name="iBrew"):
        print "iBrew: Domoticz Setup"
        self.domoticzurl = connection
        self.hardwarename = name
        client.device_type()
        print "Appliance: " + Smarter.device_info(client.deviceId,client.version) + " [" + client.host + ":" + str(client.port) + "]"
        print "Domoticz connection: [" + connection + "]"
        if self.check_hardware():
            print "Domoticz hardware: " + self.hardwarename + " [" + str(self.hardwareid) + "]"

        if client.isKettle:
            client.triggerAdd("Domoticz","TEMPERATURE",url_trigger_value % (self.domoticzurl,""))
            client.triggerAdd("Domoticz","WATERSENSOR",url_trigger_value % (self.domoticzurl,""))
            client.triggerAdd("Domoticz","KETTLEBUSY",url_trigger_switch % (self.domoticzurl,""))
            client.triggerAdd("Domoticz","KEEPWARM",url_trigger_switch % (self.domoticzurl,""))
            client.triggerAdd("Domoticz","KETTLEHEATER",url_trigger_switch % (self.domoticzurl,""))
            client.triggerAdd("Domoticz","FORMULACOOLING",url_trigger_switch % (self.domoticzurl,""))
            client.triggerAdd("Domoticz","ONBASE",url_trigger_switch % (self.domoticzurl,""))
            client.triggerAdd("Domoticz","KETTLESTATUS",url_trigger_value % (self.domoticzurl,""))
            client.triggerAdd("Domoticz","KETTLEDEFAULTCHANGED",url_trigger_switch % (self.domoticzurl,""))
            client.triggerAdd("Domoticz","BASECHANGED",url_trigger_switch % (self.domoticzurl,""))
            client.triggerAdd("Domoticz","BASE",url_trigger_user % (self.domoticzurl,""))
            client.triggerAdd("Domoticz","DEFAULTTEMPERATURE",url_trigger_user % (self.domoticzurl,""))
            client.triggerAdd("Domoticz","DEFAULTFORMULATEMPERATURE",url_trigger_user % (self.domoticzurl,""))
            client.triggerAdd("Domoticz","DEFAULTKEEPWARM",url_trigger_user % (self.domoticzurl,""))
            client.triggerAdd("Domoticz","DEFAULTKEEPWARMTEXT",url_trigger_user % (self.domoticzurl,""))

        if client.isCoffee:
            client.triggerAdd("Domoticz","CARAFE",url_trigger_switch % (self.domoticzurl,""))
            client.triggerAdd("Domoticz","READY",url_trigger_switch % (self.domoticzurl,""))
            client.triggerAdd("Domoticz","WORKING",url_trigger_switch % (self.domoticzurl,""))
            client.triggerAdd("Domoticz","ENOUGHWATER",url_trigger_switch % (self.domoticzurl,""))
            client.triggerAdd("Domoticz","CARAFEREQUIRED",url_trigger_switch % (self.domoticzurl,""))
            client.triggerAdd("Domoticz","COFFEEBUSY",url_trigger_switch % (self.domoticzurl,""))
            client.triggerAdd("Domoticz","COFFEEHEATER",url_trigger_switch % (self.domoticzurl,""))
            client.triggerAdd("Domoticz","GRINDER",url_trigger_switch % (self.domoticzurl,""))
            client.triggerAdd("Domoticz","HOTPLATE",url_trigger_switch % (self.domoticzurl,""))
            client.triggerAdd("Domoticz","COFFEEDEFAULTCHANGED",url_trigger_switch % (self.domoticzurl,""))
            client.triggerAdd("Domoticz","COFFEESETTINGSCHANGED",url_trigger_switch % (self.domoticzurl,""))
            client.triggerAdd("Domoticz","MODE",url_trigger_switch % (self.domoticzurl,""))
            client.triggerAdd("Domoticz","COFFEESTATUS",url_trigger_value % (self.domoticzurl,""))
            client.triggerAdd("Domoticz","WATERLEVELTEXT",url_trigger_value % (self.domoticzurl,""))
            client.triggerAdd("Domoticz","COFFEESTATUS",url_trigger_value % (self.domoticzurl,""))
            client.triggerAdd("Domoticz","MODETEXT",url_trigger_value % (self.domoticzurl,""))
            client.triggerAdd("Domoticz","GRINDTEXT",url_trigger_value % (self.domoticzurl,""))
            client.triggerAdd("Domoticz","STRENGTHTEXT",url_trigger_value % (self.domoticzurl,""))
            client.triggerAdd("Domoticz","CUPSTEXT",url_trigger_value % (self.domoticzurl,""))
            client.triggerAdd("Domoticz","CUPSBREW",url_trigger_user % (self.domoticzurl,""))
            client.triggerAdd("Domoticz","GRIND",url_trigger_user % (self.domoticzurl,""))
            client.triggerAdd("Domoticz","STRENGTH",url_trigger_user % (self.domoticzurl,""))
            client.triggerAdd("Domoticz","CUPS",url_trigger_user % (self.domoticzurl,""))
            client.triggerAdd("Domoticz","WATERLEVEL",url_trigger_user % (self.domoticzurl,""))
            client.triggerAdd("Domoticz","DEFAULTCUPS",url_trigger_user % (self.domoticzurl,""))
            client.triggerAdd("Domoticz","DEFAULTCUPSTEXT",url_trigger_user % (self.domoticzurl,""))
            client.triggerAdd("Domoticz","DEFAULTSTRENGTH",url_trigger_user % (self.domoticzurl,""))
            client.triggerAdd("Domoticz","DEFAULTSTRENGTHTEXT",url_trigger_user % (self.domoticzurl,""))
            client.triggerAdd("Domoticz","DEFAULTGRIND",url_trigger_user % (self.domoticzurl,""))
            client.triggerAdd("Domoticz","DEFAULTGRINDTEXT",url_trigger_user % (self.domoticzurl,""))
            client.triggerAdd("Domoticz","DEFAULTHOTPLATE",url_trigger_user % (self.domoticzurl,""))
            client.triggerAdd("Domoticz","DEFAULTHOTPLATETEXT",url_trigger_user % (self.domoticzurl,""))

        client.boolsGroup("Domoticz",[0],"On")

Domoticz = iBrewDomoticz()

