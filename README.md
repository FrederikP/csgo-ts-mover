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
- Python3 (with the following libraries: flask, ts3, PyYAML; I recommend using virtualenv to isolate the runtime environment)
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
- ts-mover-service-config.yaml
  - should be in the folder you start the service in
  - main configuration file (example is in repository)
  - the mapping maps steamid -> teamspeak client unique id (cluid; looks like this: yXM6PUfbCcPU+joxIFek1xOQwwQ=)
  - channel ids take care of where players are put (ids cannot be found in teamspeak client, use a tool like YaTQA)
  - lobby threshold determines the minimum number to swap players into the t and ct channels (there is an issue, see [#2](https://github.com/FrederikP/csgo-ts-mover/issues/2))

### Tutorial

#### Intro

This tutorial is supposed to be a simple entry point for admins who don't really know where to start. I wouldn't recommend setting everything up like
this forever. In this tutorial we won't use docker for example even though I recommend to use it, especially when running many different game servers or other
services on your server. I try to keep this tutorial as simple as possible. Everything will happen on the command line and no web admin frontend (like plesk) 
will be required. This should give everyone the same chance to get the csgo-ts-mover setup going.

I will use Ubuntu/Debian as an example linux distro, because it is often used in the game server world. If you are running a different distro you'll need to 
adjust some of the commands to your needs (for example when installing dependencies.)

#### Requirements

- sudo rights on your server
- csgo server with sourcemod installed
- RipExt source mod library installed (see https://github.com/ErikMinekus/sm-ripext)
- debian based system (if you have a different base, please adjust package installation command accordingly, rest should work as well)

#### Steps

1. Download package requirements for this tutorial

   ```
   sudo apt update

   ### Run this to upgrade existing packages on your system (often a good idea..., but not really part of this tutorial):
   # sudo apt upgrade

   sudo apt install wget screen python3-pip python3-virtualenv
   ```

1. Change directories to your csgo sourcemod plugins directory and download the plugin from the releases page. Replace `[...]` with your actual path prefix

   ```bash
   cd [...]/csgo/csgo/addons/sourcemod/plugins/
   wget https://github.com/FrederikP/csgo-ts-mover/releases/download/0.1.0/ts-mover.smx
   ```

1. Run your csgo server to generate the config file at `[...]/csgo/csgo/cfg/sourcemod/ts-mover.cfg`. If you follow this tutorial, you shouldn't need to edit the file for now.

1. Create a new empty directory somewhere on your server (e.g. your home dir). It should not be part of the csgo installation.

   ```bash
   mkdir ~/csgo-ts-mover
   cd ~/csgo-ts-mover
   ```

1. Download the server code and the example config from github

   ```bash
   wget https://raw.githubusercontent.com/FrederikP/csgo-ts-mover/master/ts-mover-service.py
   wget https://raw.githubusercontent.com/FrederikP/csgo-ts-mover/master/ts-mover-service-config.yaml
   ```

1. Adjust the `ts-mover-service-config.yaml` to your needs. The configuration values are explained in the example file.

   ```bash
   edit ts-mover-service-config.yaml
   ```

1. Initialize and activate a python3 virtualenv to keep the python dependencies separated from other stuff on your system

   ```bash
   ### From here on out we'll use a screen session, so we can later detach it and keep it running. We can then also re-attach to it later to read logs, etc.
   screen -S csgo-ts-mover
   ### Your terminal will be cleared at this point

   ### Create virtualenv in venv subfolder
   virtualenv -p python3 venv

   ### Activate virtualenv (the dot is important)
   . venv/bin/activate
   ```

1. Install python dependencies

   ```bash
   pip install flask ts3 PyYAML
   ```

1. Start the server (at the end of this step, the csgo plugin has someone to talk to)

   ```bash
   export FLASK_APP=ts-mover-service.py
   ### Note: If you want need the service to listen on other interfaces (default is localhost) use --host 0.0.0.0 or --host <IP> .
   ### For this simple tutorial, the following should suffice
   flask run --port 6666
   ### You should now see logs of the csgo-ts-mover server
   ```

1. Try out your setup by playing csgo
   - You should see log entries when connecting to the server
   - You can detach and keep the ts-mover-service running using CTRL-A + D (see screen manual)
   - You can reattach using `screen -r csgo-ts-mover`
   - When attached you can stop the server with CTRL-C. Do that and start again when you changes the config file
   - When you encounter issues please provide logs from the csgo-ts-mover and logs from your csgo server

## Things to note
- If the teamspeak server is running on a different host than the web service, then the IP of the web service should be whitelisted in teamspeak. For more see the teamspeak query docs.
- If you need authentication and encryption for the web service, use a web server like nginx or apache to proxy traffic
- I use docker to run the csgo servers as well as the service and it makes things a lot easier. I see the following advantages:
  - Isolation (well duh) - Actually run multiple csgo servers on one host without getting confused
  - Reproducabilty (very important when trying to figure out to run many different plugins)

## Future ideas
- Allow mapping configuration using chat commands in csgo
- Kick players that are not in the mapping automatically

## Contributing
- Feel free to open merge requests if you have improvements! Looking forward to it.
