# csgo-ts-mover
Moves players to teamspeak channels according to the team they are on. Especially fun for retake and similar game modes.

## Overview
The provided functionality is realized using two components. The first component is a sourcemod plugin. This plugin is only responsible for communicating team changes. The other component is a web service that talks with the teamspeak server and reacts to the change information received by the sourcemod plugin.

## Setup

### Requirements

- Sourcemod (https://www.sourcemod.net/downloads.php)
- RipExt (https://github.com/ErikMinekus/sm-ripext)
- Python3 (with the following libraries: flask, ts3)
- Teamspeak with Query Login Credentials

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
