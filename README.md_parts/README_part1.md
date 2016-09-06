# iBrew Kettle Rattle

[iKettle 2.0](http://smarter.am/ikettle) and [Smarter Coffee](http://smarter.am/coffee) Interface


## Introduction
iBrew is a (python) interface to iKettle 2.0 and Smarter Coffee devices. It includes a console, monitor, command line interface, web interface and rest api. You can also use it in your own code. iKettle 2.0 v19 and SmarterCoffee v20 tested at the moment. Please share any other discoveries you made!

This means your machine is free! You can connect it yourself and do whatever you want with it. Like interface it with your favorite smarthome controller!

   Signed Me!

#### Versions
 * v0.0 Bean Grinder Pack
 * v0.1 White Tealeaf Edition
 * v0.2 Tea Noire Sweet
 * v0.3 Kettle Rattle <-- CURRENT VERSION
 * v0.4 Brewing on the 7th day (web interface) 
 * v0.5 Dumb Dump Limited Collector Edition (numbered, signed by author)
 * v1.0 Out of order! (the final cut) <-- 2017 NEVER TOUCH THE CODE AGAIN VERSION
 
#### Upcoming for the last 3 versions  
 * Timers protocol
 * Time arguments (have not figured that out)
 * Better error handling (sometimes it does not quit :-)
 * it also hangs if you scan wifi too much (luckily it reconnects)
 * Connecting in console mode... fails sometimes, and after reconnect is had strange data... stupid threads... missing...
 * Web interface & rest api (rest almost finished, web interface still have to create some pages) and introduce webroot & api key,...,...
 * History message is not finished
 * Fahrenheid not finished, please to not use.
 * v0.5 Missing Coffee Smarter codes (!)
 * messages everywhere from the monitor...
 * fix wireless with the same name
 * watersensor to something usefull
 * process what you get back... (03 responses)
 
#### Contact
[Bugs or issues](https://github.com/Tristan79/iBrew/issues). Donations & other questions <tristan@monkeycat.nl>
If you have jokes on coffee, tea, hot chocolade, coffee machines or kettles, please post in the issues.

Still no coffee machine (so no web for that)! I could like to thank Ju4ia for letting me access his coffee machine remotely, so I could test the client code and helping me
get more SmarterCoffee missing protocol stuff.


## Installation

#### Software Requirements 

* python 2.7
* python package: wireless
* python (optional) package: tornado 
* python (optional) package: pybonjour

#### Download
You can download and unpack the [source](https://github.com/Tristan79/iBrew/archive/master.zip) or download it from github using [Github Desktop](https://desktop.github.com) or manually:

```
git clone https://github.com/Tristan79/iBrew.git
```

#### Setup

Run ```make``` or ```pip install -r requirements.txt``` to fetch missing python packages...

## Usage

### Command Line

See the console section for the commands
 
```