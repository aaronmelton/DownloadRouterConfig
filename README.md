# Download Router Config

A Python script to capture the running-config of Cisco Routers and Switches.

## Getting Started

### About This Code
This script was originally written in Python2 and relied on [Exscript](https://github.com/knipknap/exscript/) to handle all the 'heavy lifting' of communicating with the router.

However, it appears that Exscript went the way of Python2 and is no longer supported.

In conjunction with updating this code to work with Python3, I've also selected [NAPALM](https://github.com/ktbyers/napalm) to replace the functionality that Exscript once provided.

#### Requirements
1. This application is hard-coded to use the SSH2 protocol; If SSH v2 is not enabled on your router(s), you will need to add `ip ssh version 2` to your Cisco router(s) configuration and any associated access-list changes.
2. A valid username/password.
3. A text file containing hostnames or IP Addresses of your routers/switches, one entry per line.
4. Environment variables for logging (LOG_LEVEL, LOG_PATH, LOG_PREFIX) OR you can hard-code the log_dict{} variables in config.py.

#### Assumptions
1. This application was written for use on Cisco IOS devices and cannot be guaranteed to work on other makes/model routers.
2. This application assumes that you have enable privileges on each router in order to execute the `show running-config` command.  If you do not have sufficient user privileges, this application will not work as designed.

#### Limitations
1. This application uses the same username/password to access ALL routers. If your routers use unique usernames/passwords, then this script will not work.

#### Python Libraries
* See [pyproject.toml](pyproject.toml)

### Instructions For Use

`python download_router_config.py --help`  for help.

Use `--device_list <filename>` to specify input file.
   
Use `--backup_to <path>` to specifiy where to save config files.

## Authors
* **Aaron Melton** - *Author* - Aaron Melton <aaron@aaronmelton.com>
