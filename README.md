[![Build Status](https://travis-ci.org/FrederikP/csgo-ts-mover.svg?branch=master)](https://travis-ci.org/FrederikP/csgo-ts-mover)

# csgo-ts-mover
Moves players to teamspeak channels according to the team they are on. Especially fun for retake and similar game modes.

## Overview
The provided functionality is realized using two components. The first component is a sourcemod plugin. This plugin is only responsible for communicating team changes. The other component is a web service that talks with the teamspeak server and reacts to the change information received by the sourcemod plugin.
Basically the information flow for team changes looks like this:

[CSGO] -> [ts-mover SourceMod Plugin] -> [ts-mover Service] -> [Teamspeak]

## Setup

### Requirements

- Sourcemod (https://www.sourcemod.net/downloads.php)
- RipExt (https://github.com/ErikMinekus/sm-ripext)
- Python3 (with the following libraries: flask, ts3; I recommend using virtualenv to isolate the runtime environment)
- Teamspeak with Query Login Credentials

### Essential Files
- ts-mover.smx
  - should be in csgo/csgo/addons/sourcemod/plugins/
  - the compiled sourcemod plugin
  - obtained from releases page https://github.com/FrederikP/csgo-ts-mover/releases 
  - or by compiling from yourself
- ts-mover.cfg
  - should be in csgo/csgo/cfg/sourcemod
  - is automatically created on first start of sourcemod plugin
  - allows changing http endpoint for communication with service
  - sm_ts_mover_endpoint defaults to http://localhost:6666
- ts-mover-service.py 
  - the web service that handles channel movement
- ts-mover-service-config.json
  - should be in the folder you start the service in
  - main configuration file (example is in repository)

### Starting the service

- put ts-mover.smx (see Releases) into the plugins folder of your sourcemod installation
- customize your configuration
  - the mapping maps steamid -> teamspeak nickname
  - channel names take care of where players are put
  - lobby threshold determines the minimum number to swap players into the t and ct channels
- start the service (config file should be in the same folder):

```
FLASK_APP=ts-mover-service.py
flask run --port 6666
```

Use screen, or docker, or whatever to keep it running.

# Things to note
- If the teamspeak server is running on a different host than the web service, then the IP of the web service should be whitelisted in teamspeak. For more see the teamspeak query docs.
- If you need authentication and encryption for the web service, use a web server like nginx or apache to proxy traffic
- I use docker to run the csgo servers as well as the service and it makes things a lot easier. I see the following advantages:
  - Isolation (well duh) - Actually run multiple csgo servers on one host without getting confused
  - Reproducabilty (very important when trying to figure out to run many different plugins)

# Future ideas
- Allow mapping configuration using chat commands in csgo
- Kick players that are not in the mapping automatically

# Contributing
- Feel free to open merge requests if you have improvements! Looking forward to it.