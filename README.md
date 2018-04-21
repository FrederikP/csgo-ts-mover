# csgo-ts-mover
Moves players to teamspeak channels according to the team they are on. Especially fun for retake and similar game modes.

## Overview
The provided functionality is realized using two components. The first component is a sourcemod plugin. This plugin is only responsible for communicating team changes. The other component is a web service that talks with the teamspeak server and reacts to the change information received by the sourcemod plugin.

## Setup

### Requirements

- Sourcemod (https://www.sourcemod.net/downloads.php)
- RipExt (https://github.com/ErikMinekus/sm-ripext)
- Python3 (with the following libraries: flask, ts3; I recommend using virtualenv to isolate the runtime environment)
- Teamspeak with Query Login Credentials

### Essential Files
- ts-mover.smx 
  - the compiled sourcemod plugin
  - obtained from releases page https://github.com/FrederikP/csgo-ts-mover/releases 
  - or by compiling from yourself
- ts-mover.cfg
  - is automatically created on first start of sourcemod plugin
  - allows changing http endpoint for communication with service
  - sm_ts_mover_endpoint defaults to http://localhost:6666
- ts-mover-service.py 
  - the web service that handles channel movement
- ts-mover-service-config.json
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
- If the teamspeak server is running on a different host than the web service, then the IP of the web service should be whitelisted in teamspeak. For mor see the teamspeak query docs.
- If you need authentication and encryption for the web service, use a web server like nginx or apache to proxy traffic

# Future ideas
- Allow mapping configuration using chat commands in csgo
- Kick players that are not in the mapping automatically

# Contributing
- Feel free to open merge requests if you have improvements! Looking forward to it.