# -*- coding: utf-8 -*-

import traceback
import string
import datetime
import os
import sys
import logging
import json
import urllib

from ConfigParser import *

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

url_hardware_add = 'http://%s/json.htm?type=command&param=addhardware&htype=15&port=1&name=%s&enabled=true'
url_hardware = 'http://%s/json.htm?type=hardware'
url_sensor = 'http://%s/json.htm?type=devices&order=Name'
url_sensor_add = 'http://%s/json.htm?type=createvirtualsensor&idx=%s&sensorname=%s&sensortype=%s'
url_sensor_ren = 'http://%s/json.htm?type=command&param=renamedevice&idx=%s&name=%s'
url_trigger_value = 'http://%s/json.htm?type=command&param=udevice&idx=%s&nvalue=0&svalue=§N'
url_trigger_switch = 'http://%s/json.htm?type=command&param=switchlight&idx=%s&switchcmd=§N'
#url_trigger_user = 'http://%s/json.htm?type=command&param=updateuservariable&vname=%s&vtype=0&vvalue=§N'

url_switch_type = 'http://%s/json.htm?type=setused&idx=%s&switchtype=%s&name=%s&description=&strparam1=&strparam2=&protected=false&customimage=%s&used=true&addjvalue=0&options='
url_custom_type = 'http://%s/json.htm?type=setused&idx=%s&switchtype=0&name=%s&description=&customimage=%s&used=true'

class iBrewDomoticz:

    SensorText        = 5
    SensorSwitch      = 6
    SensorTemperature = 80
    SensorCustom      = 1004

    SwitchTypeNormal  = 0
    SwitchTypeMotion  = 8
    SwitchtypeDimmer  = 7
    SwitchTypeContact = 2
    
    CustomImageNormal = 0
    CustomimageWater  = 11
    CustomImageAlarm  = 13
    CustomimageTree   = 14
    CustomImageHeating = 15
    CustomImageCooling = 16
    
    def open_url(self,url):
        if self.dump:
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

    def __init__(self,connection="127.0.0.1:8080",name="NaNa"):
        self.domoticzurl = connection
        self.hardwarename = name
        self.write_config = False
        self.prefix = ""
        self.query = True
    
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
        if self.query:
            response = self.open_url(url_sensor % (self.domoticzurl))
            if response == 'None':
                return 'None'
            self.data = json.loads(response.read())
            self.query = False
        if 'result' in self.data:
            for i in range(0,len(self.data['result'])):
                if name == self.data['result'][i]['Name'] and int(self.hardwareid) == self.data['result'][i]['HardwareID']:
                    return self.data['result'][i]['idx']
        return 'None'

    def exists_id(sensorid):
        if self.query:
            response = self.open_url(url_sensor % (self.domoticzurl))
            if response == 'None':
                return 'None'
            self.data = json.loads(response.read())
            self.query = False
        if 'result' in self.data:
            for i in range(0,len(self.data['result'])):
                if sensorid == self.data['result'][i]['idx'] and int(self.hardwareid) == self.data['result'][i]['HardwareID']:
                    return True
        return False


    def use_virtual_sensor(self,name,type,options=''):
        sensorid = self.exists_sensor(name)
        if 'None' != sensorid:
            return sensorid
        if 'None' == sensorid:
            url = url_sensor_add % (self.domoticzurl, self.hardwareid, name.replace(' ', '%20'),str(type))
            if options != '':
                url = url + '&sensoroptions=' + options
            response = self.open_url(url)
            self.query = True
            return self.exists_sensor(name)
            
            
    def get_id(self,iniid,text,type,options=""):
        try:
            rid = self.config.get(self.section, iniid)
            if not exists_id(id):
                raise Exception
        except:
            if self.prefix == "":
                t = text
            else:
                t = self.prefix + " " + text
            rid = self.use_virtual_sensor(t,type,options)
            if rid == 'None':
                logging.error('iBrew: Domoticz: Unable to access Domoticz sendor: ' + self.prefix + " " + text)
            self.config.set(self.section, iniid, rid)
            write_config = True
        return rid

    def set_switch_type(self,idx,name,switchType,switchImage):
        n = name
        if self.prefix != "":
            n = self.prefix + " " + name
        url = url_switch_type % (self.domoticzurl,idx,str(switchType),n.replace(' ', '%20'),str(switchImage))
        self.open_url(url)


    def set_custom_type(self,idx,name,switchImage):
        n = name
        if self.prefix != "":
            n = self.prefix + " " + name
        url = url_custom_type % (self.domoticzurl,idx,n.replace(' ', '%20'),str(switchType))
        self.open_url(url)


        
    def setup(self,client,connection,prefix="",name=""):
        self.dump = client.dump
        self.prefix = prefix
        #client.dump = True
        print "iBrew: Domoticz Setup"
        client.device_type()
        if name == "":
            if client.isKettle: self.hardwarename = "iKettle 2.0"
            elif client.isCoffee: self.hardwarename = "Smarter Coffee"
            else:
                return "iBrew: Device not supported"
            
        self.domoticzurl = connection
       
        
        print "Appliance: " + Smarter.device_to_string(client.deviceId) + " [" + client.host + ":" + str(client.port) + "]"
        print "Domoticz connection: [" + connection + "]"
        if self.check_hardware():
            print "Domoticz hardware: " + self.hardwarename + " [" + str(self.hardwareid) + "]"


        self.config = SafeConfigParser()
        if not os.path.exists(client.settingsPath):
                os.makedirs(client.settingsPath)
        self.section = client.host + "." + str(client.port) + ".domoticz"
        self.config.read(client.settingsPath+'ibrew.conf')
        try:
            self.config.add_section(self.section)
        except DuplicateSectionError:
            pass


            
        if client.isKettle:
            id = self.get_id('TEMPERATURE','Temperature',self.SensorTemperature)
            client.triggerAdd("Domoticz","TEMPERATURE",url_trigger_value % (self.domoticzurl,id))
            client.boolsGroup("Domoticz","On")
            id = self.get_id('WATERSENSOR','Water Level',self.SensorCustom,";")
            self.set_switch_type(id,'Water Level',self.SwitchTypeNormal,self.CustomimageWater)
            client.triggerAdd("Domoticz","WATERSENSOR",url_trigger_value % (self.domoticzurl,id))
            id = self.get_id('KETTLEBUSY','Busy',self.SensorSwitch)
            self.set_switch_type(id,'Busy',self.SwitchTypeMotion,self.CustomImageNormal)
            client.triggerAdd("Domoticz","KETTLEBUSY",url_trigger_switch % (self.domoticzurl,id))
            id = self.get_id('KEEPWARM','Keep Warm Time',self.SensorSwitch)
            self.set_switch_type(id,'Keep Warm Time',self.SwitchTypeMotion,self.CustomImageNormal)
            client.triggerAdd("Domoticz","KEEPWARM",url_trigger_switch % (self.domoticzurl,id))
            id = self.get_id('KETTLEHEATER','Heater',self.SensorSwitch)
            self.set_switch_type(id,'Heater',self.SwitchTypeMotion,self.CustomImageHeating)
            client.triggerAdd("Domoticz","KETTLEHEATER",url_trigger_switch % (self.domoticzurl,id))
            id = self.get_id('FORMULACOOLING','Formula Cooling',self.SensorSwitch)
            self.set_switch_type(id,'Formula Cooling',self.SwitchTypeMotion,self.CustomImageNormal)
            client.triggerAdd("Domoticz","FORMULACOOLING",url_trigger_switch % (self.domoticzurl,id))
            id = self.get_id('OFFBASE','Off Base',self.SensorSwitch)
            self.set_switch_type(id,'Off Base',self.SwitchTypeMotion,self.CustomImageCooling)
            client.triggerAdd("Domoticz","OFFBASE",url_trigger_switch % (self.domoticzurl,id))
            id = self.get_id('STATUS','Status',self.SensorText)
            client.triggerAdd("Domoticz","KETTLESTATUS",url_trigger_value % (self.domoticzurl,id))
            id = self.get_id('KETTLEDEFAULTCHANGED','Settings Changed',self.SensorSwitch)
            self.set_switch_type(id,'Settings Changed',self.SwitchTypeMotion,self.CustomImageNormal)
            client.triggerAdd("Domoticz","KETTLEDEFAULTCHANGED",url_trigger_switch % (self.domoticzurl,id))
            id = self.get_id('BASECHANGED','Calibration Changed',self.SensorSwitch)
            self.set_switch_type(id,'Calibration Changed',self.SwitchTypeMotion,self.CustomImageNormal)
            client.triggerAdd("Domoticz","BASECHANGED",url_trigger_switch % (self.domoticzurl,id))
            id = self.get_id('BASE','Calibration Base',self.SensorCustom,";")
            client.triggerAdd("Domoticz","BASE",url_trigger_value % (self.domoticzurl,id))
            id = self.get_id('DEFAULTTEMPERATURE','Default Temperature',self.SensorTemperature)
            client.triggerAdd("Domoticz","DEFAULTTEMPERATURE",url_trigger_value % (self.domoticzurl,id))
            id = self.get_id('DEFAULTFORMULATEMPERATURE','Default Formula Temperature',self.SensorTemperature)
            client.triggerAdd("Domoticz","DEFAULTFORMULATEMPERATURE",url_trigger_value % (self.domoticzurl,id))
            id = self.get_id('DEFAULTKEEPWARM','Default Keep Warm Value',self.SensorCustom,";minutes")
            client.triggerAdd("Domoticz","DEFAULTKEEPWARM",url_trigger_value % (self.domoticzurl,id))
            id = self.get_id('DEFAULTKEEPWARMTEXT','Default Keep Warm',self.SensorCustom,";minutes")
            client.triggerAdd("Domoticz","DEFAULTKEEPWARMTEXT",url_trigger_value % (self.domoticzurl,id))

        if client.isCoffee:
            id = self.get_id('COFFEESTATUS','Status',self.SensorText)
            client.triggerAdd("Domoticz","COFFEESTATUS",url_trigger_value % (self.domoticzurl,id))
            client.boolsGroup("Domoticz","On")
            id = self.get_id('CARAFE','Carafe',self.SensorSwitch)
            self.set_switch_type(id,'Carafe',self.SwitchTypeMotion,self.CustomImageNormal)
            client.triggerAdd("Domoticz","CARAFE",url_trigger_switch % (self.domoticzurl,id))
            id = self.get_id('READY','Ready',self.SensorSwitch)
            self.set_switch_type(id,'Ready',self.SwitchTypeMotion,self.CustomImageNormal)
            client.triggerAdd("Domoticz","READY",url_trigger_switch % (self.domoticzurl,id))
            id = self.get_id('WORKING','Working',self.SensorSwitch)
            self.set_switch_type(id,'Working',self.SwitchTypeMotion,self.CustomImageNormal)
            client.triggerAdd("Domoticz","WORKING",url_trigger_switch % (self.domoticzurl,id))
            id = self.get_id('ENOUGHWATER','Enough Water',self.SensorSwitch)
            self.set_switch_type(id,'Enough water',self.SwitchTypeMotion,self.CustomImageNormal)
            client.triggerAdd("Domoticz","ENOUGHWATER",url_trigger_switch % (self.domoticzurl,id))
            id = self.get_id('CARAFEREQUIRED','Carafe Required',self.SensorSwitch)
            self.set_switch_type(id,'Carafe Required',self.SwitchTypeMotion,self.CustomImageNormal)
            client.triggerAdd("Domoticz","CARAFEREQUIRED",url_trigger_switch % (self.domoticzurl,id))
            id = self.get_id('COFFEEBUSY','Busy',self.SensorSwitch)
            self.set_switch_type(id,'Busy',self.SwitchTypeMotion,self.CustomImageNormal)
            client.triggerAdd("Domoticz","COFFEEBUSY",url_trigger_switch % (self.domoticzurl,id))
            id = self.get_id('COFFEEHEATER','Heater',self.SensorSwitch)
            self.set_switch_type(id,'Heater',self.SwitchTypeMotion,self.CustomImageNormal)
            client.triggerAdd("Domoticz","COFFEEHEATER",url_trigger_switch % (self.domoticzurl,id))
            id = self.get_id('GRINDER','Grinder',self.SensorSwitch)
            self.set_switch_type(id,'Grinder',self.SwitchTypeMotion,self.CustomImageNormal)
            client.triggerAdd("Domoticz","GRINDER",url_trigger_switch % (self.domoticzurl,id))
            id = self.get_id('HOTPLATE','Hotplate',self.SensorSwitch)
            self.set_switch_type(id,'Hotplate',self.SwitchTypeMotion,self.CustomImageNormal)
            client.triggerAdd("Domoticz","HOTPLATE",url_trigger_switch % (self.domoticzurl,id))
            id = self.get_id('COFFEEDEFAULTCHANGED','Default Settings Changed',self.SensorSwitch)
            self.set_switch_type(id,'Default Settings Changed',self.SwitchTypeMotion,self.CustomImageNormal)
            client.triggerAdd("Domoticz","COFFEEDEFAULTCHANGED",url_trigger_switch % (self.domoticzurl,id))
            id = self.get_id('COFFEESETTINGSCHANGED','Settings Changed',self.SensorSwitch)
            self.set_switch_type(id,'Settings Changed',self.SwitchTypeMotion,self.CustomImageNormal)
            client.triggerAdd("Domoticz","COFFEESETTINGSCHANGED",url_trigger_switch % (self.domoticzurl,id))
            id = self.get_id('GRIND','Grind Value',self.SensorSwitch)
            self.set_switch_type(id,'Grind Value',self.SwitchTypeMotion,self.CustomImageNormal)
            client.triggerAdd("Domoticz","GRIND",url_trigger_value % (self.domoticzurl,id))
            id = self.get_id('DEFAULTGRIND','Default Grind Value',self.SensorSwitch)
            self.set_switch_type(id,'Default Grind Value',self.SwitchTypeMotion,self.CustomImageNormal)
            client.triggerAdd("Domoticz","DEFAULTGRIND",url_trigger_value % (self.domoticzurl,id))
            id = self.get_id('MODE','Mode Value',self.SensorSwitch)
            self.set_switch_type(id,'Mode Value',self.SwitchTypeMotion,self.CustomImageNormal)
            client.triggerAdd("Domoticz","MODE",url_trigger_switch % (self.domoticzurl,id))

            id = self.get_id('WATERLEVELTEXT','Water Level',self.SensorText)
            client.triggerAdd("Domoticz","WATERLEVELTEXT",url_trigger_value % (self.domoticzurl,id))
            id = self.get_id('MODETEXT','Mode',self.SensorText)
            client.triggerAdd("Domoticz","MODETEXT",url_trigger_value % (self.domoticzurl,id))
            id = self.get_id('GRINDTEXT','Grind',self.SensorText)
            client.triggerAdd("Domoticz","GRINDTEXT",url_trigger_value % (self.domoticzurl,id))
            id = self.get_id('STRENGTHTEXT','Strength',self.SensorText)
            client.triggerAdd("Domoticz","STRENGTHTEXT",url_trigger_value % (self.domoticzurl,id))
            id = self.get_id('CUPSBREW','Cups Brewed Value',self.SensorCustom,";cups")
            client.triggerAdd("Domoticz","CUPSBREW",url_trigger_value % (self.domoticzurl,id))
            id = self.get_id('STRENGTH','Strength Value',self.SensorCustom,";")
            client.triggerAdd("Domoticz","STRENGTH",url_trigger_value % (self.domoticzurl,id))
            id = self.get_id('CUPS','Cups Value',self.SensorCustom,";cups")
            client.triggerAdd("Domoticz","CUPS",url_trigger_value % (self.domoticzurl,id))
            id = self.get_id('CUPSTEXT','Cups',self.SensorText)
            client.triggerAdd("Domoticz","CUPSTEXT",url_trigger_value % (self.domoticzurl,id))
            id = self.get_id('DEFAULTCUPSTEXT','Default Cups',self.SensorText)
            client.triggerAdd("Domoticz","DEFAULTCUPSTEXT",url_trigger_value % (self.domoticzurl,id))
            id = self.get_id('CUPSBREWTEXT','Cups Brewed',self.SensorText)
            client.triggerAdd("Domoticz","CUPSBREWTEXT",url_trigger_value % (self.domoticzurl,id))

            id = self.get_id('WATERLEVEL','Water Level Value',self.SensorCustom,";")
            client.triggerAdd("Domoticz","WATERLEVEL",url_trigger_value % (self.domoticzurl,id))
            id = self.get_id('DEFAULTCUPS','Default Cups Value',self.SensorCustom,";cups")
            client.triggerAdd("Domoticz","DEFAULTCUPS",url_trigger_value % (self.domoticzurl,id))
            id = self.get_id('DEFAULTSTRENGTH','Default Strenght Value',self.SensorText)
            client.triggerAdd("Domoticz","DEFAULTSTRENGTH",url_trigger_value % (self.domoticzurl,id))
            id = self.get_id('DEFAULTSTRENGTHTEXT','Default Strength',self.SensorText)
            client.triggerAdd("Domoticz","DEFAULTSTRENGTHTEXT",url_trigger_value % (self.domoticzurl,id))
            id = self.get_id('DEFAULTGRINDTEXT','Default Grind',self.SensorText)
            client.triggerAdd("Domoticz","DEFAULTGRINDTEXT",url_trigger_value % (self.domoticzurl,id))
            id = self.get_id('DEFAULTHOTPLATE','Default Hotplate Time Value',self.SensorCustom,";minutes")
            client.triggerAdd("Domoticz","DEFAULTHOTPLATE",url_trigger_value % (self.domoticzurl,id))
            id = self.get_id('DEFAULTHOTPLATETEXT','Default Hotplate Time',self.SensorText)
            client.triggerAdd("Domoticz","DEFAULTHOTPLATETEXT",url_trigger_value % (self.domoticzurl,id))

        #client.dump = self.dump


Domoticz = iBrewDomoticz()

