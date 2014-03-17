#!/usr/bin/env python
#
# DownloadRouterConfig.py
# Copyright (C) 2012-2014 Aaron Melton <aaron(at)aaronmelton(dot)com>
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.


import argparse     # Required to read arguments from the command line
import base64       # Required to decode password
import datetime     # Required for date format
import ConfigParser # Required for configuration file
import Exscript     # Required for SSH, queue & logging functionality
import re           # Required for REGEX operations
import sys          # Required for printing without newline
import os           # Required to determine OS of host

from argparse                   import ArgumentParser, RawDescriptionHelpFormatter
from base64                     import b64decode
from ConfigParser               import ConfigParser
from datetime                   import datetime
from Exscript                   import Account, Queue, Host, Logger
from Exscript.protocols         import SSH2
from Exscript.util.file         import get_hosts_from_file
from Exscript.util.log          import log_to
from Exscript.util.decorator    import autologin
from Exscript.util.interact     import read_login
from Exscript.util.report       import status,summarize
from re                         import search, sub
from sys                        import stdout
from os                         import getcwd, makedirs, name, path, system


class Application:
# This class was created to provide me with an easy way to update application
# details across all my applications.  Also used to display information when
# application is executed with "--help" argument.
    author = "Aaron Melton <aaron@aaronmelton.com>"
    date = "(2014-03-17)"
    description = "Downloads the running-config of a Cisco router."
    name = "DownloadRouterConfig.py"
    version = "v2.2.3"
    url = "https://github.com/aaronmelton/DownloadRouterConfig"


logger = Logger()   # Log stuff
@log_to(logger)     # Logging decorator; Must precede downloadRouterConfig!
@autologin()        # Exscript login decorator; Must precede downloadRouterConfig!
def downloadRouterConfig(job, host, socket):
# This function logs into each of the hosts in the routerFile and writes the 
# contents of running-config to an outputFile.

    # If backupDirectory does not exist, create it
    if not path.exists(backupDirectory): makedirs(backupDirectory)

    # Define output filename based on hostname and date
    outputFilename = backupDirectory+host.get_name()+"_Config_"+date+".txt"    

    # Check to see if outputFilename currently exists.  If it does, append an
    # integer onto the end of the filename until outputFilename no longer exists
    incrementOutputFilename = 1
    while fileExist(outputFilename):
        outputFilename = backupDirectory+host.get_name()+"_Config_"+date+"_"+str(incrementOutputFilename)+".txt"
        incrementOutputFilename = incrementOutputFilename + 1

    with open(outputFilename, "w") as outputFile:
        try:
            socket.execute("terminal length 0")     # Disable user-prompt to page through config
                                                    # Exscript doesn't always recognize Cisco IOS
                                                    # for socket.autoinit() to work correctly
            socket.execute("show running-config")   # Show running config

            # Write contents of running config to output file
            outputFile.write(socket.response)
        
            socket.send("exit\r")   # Send the "exit" command to log out of router gracefully
            socket.close()          # Close SSH connection

        # Exception: output file was not able to be opened
        except IOError:
            print
            print "--> An error occurred opening "+outputFilename+"."

def fileExist(fileName):
# This function checks the parent directory for the presence of a file
# Returns true if found, false if not

    try:
        # If file can be opened, it must exist
        with open(fileName, "r") as openedFile:
            return True # File found

    # Exception: file cannot be opened, must not exist
    except IOError:
        return False    # File NOT found


# Check to determine if any arguments may have been presented at the command
# line and generate help message for "--help" switch
parser = ArgumentParser(
    formatter_class=RawDescriptionHelpFormatter,description=(
        Application.name+" "+Application.version+" "+Application.date+"\n"+
        "--\n"+
        "Description: "+Application.description+"\n\n"+
        "Author: "+Application.author+"\n"+
        "URL:    "+Application.url
    ))
# Add additional argument to handle any optional configFile passed to application
parser.add_argument("-c", "--config", dest="configFile", help="config file", default="settings.cfg", required=False)
args = parser.parse_args()      # Set "args" = input from command line
configFile = args.configFile    # Set configFile = config file from command line OR "settings.cfg"

# Determine OS in use and clear screen of previous output
if name == "nt":    system("cls")
else:               system("clear")

# PRINT PROGRAM BANNER
print Application.name+" "+Application.version+" "+Application.date
print "-"*(len(Application.name+Application.version+Application.date)+2)


# START PROGRAM
try:
# Try to open configFile
    with open(configFile, "r"):    pass
    
except IOError:
# Except if configFile does not exist, create an example configFile to work from
    try:
        with open (configFile, "w") as exampleFile:
            print
            print "--> Config file not found; Creating "+configFile+"."
            exampleFile.write("## DownloadRouterConfig.py CONFIGURATION FILE ##\n#\n")
            exampleFile.write("[account]\n#password is base64 encoded! Plain text passwords WILL NOT WORK!\n#Use website such as http://www.base64encode.org/ to encode your password\nusername=\npassword=\n#\n")
            exampleFile.write("[DownloadRouterConfig]\n#variable=C:\path\\to\\filename.ext\nrouterFile=routers.txt\nlogFileDirectory=\nbackupDirectory=\n")
            exampleFile.write("# See http://knipknap.github.io/exscript/api/Exscript.Queue-class.html#__init__\n# for information on verbose and thread settings\n")
            exampleFile.write("# Recommend verboseOutput = 1\nverboseOutput=1\n# Recommend maxThreads > 2\nmaxThreads=5\n")

    # Exception: configFile could not be created
    except IOError:
        print
        print "--> An error occurred creating the example "+configFile+"."

finally:
# Finally, using the provided configFile (or example created), pull values
# from the config and login to the router(s)
    config = ConfigParser(allow_no_value=True)
    config.read(configFile)
    username = config.get("account", "username")
    password = config.get("account", "password")
    routerFile = config.get("DownloadRouterConfig", "routerFile")
    logFileDirectory = config.get("DownloadRouterConfig", "logFileDirectory")
    backupDirectory = config.get ("DownloadRouterConfig", "backupDirectory")
    verboseOutput = config.get ("DownloadRouterConfig", "verboseOutput")
    maxThreads = config.get ("DownloadRouterConfig", "maxThreads")

    # If logFileDirectory is blank, use current working directory
    if logFileDirectory == "":  logFileDirectory = getcwd()

    # If logFileDirectory does not contain trailing backslash, append one
    if logFileDirectory != "":
        if logFileDirectory[-1:] != "\\": logFileDirectory = logFileDirectory+"\\"
            
    # If backupDirectory is blank, use current working directory
    if backupDirectory == "":  backupDirectory = getcwd()

    # If backupDirectory does not contain trailing backslash, append one
    if backupDirectory != "":
        if backupDirectory[-1:] != "\\": backupDirectory = backupDirectory+"\\"

    # Error checking for verboseOutput & maxThreads
    if int(verboseOutput) not in range(0,5):    verboseOutput = 1
    if int(maxThreads) not in range(1,100):     maxThreads = 2

    if fileExist(routerFile):
        # Define "date" variable for use in the output filename
        date = datetime.now()           # Determine today's date
        date = date.strftime("%Y%m%d")  # Format date as YYYYMMDD
    
        if username == "":              # If username is blank
            print
            account = read_login()      # Prompt the user for login credentials

        elif password == "":            # If password is blank
            print
            account = read_login()      # Prompt the user for login credentials

        else:                           # Else use username/password from configFile
            account = Account(name=username, password=b64decode(password))
    
        # Read hosts from specified file & remove duplicate entries, set protocol to SSH2
        hosts = get_hosts_from_file(routerFile, default_protocol="ssh2", remove_duplicates=True)
        
        print
        
        # Verbose & # threads taken from configFile, redirect errors to null
        queue = Queue(verbose=int(verboseOutput), max_threads=int(maxThreads), stderr=(open(os.devnull, "w")))
        queue.add_account(account)              # Use supplied user credentials
        queue.run(hosts, downloadRouterConfig)  # Create queue using provided hosts
        queue.shutdown()                        # End all running threads and close queue
    
        print status(logger)    # Print current % status of operation to screen

        # If logFileDirectory does not exist, create it.
        if not path.exists(logFileDirectory): makedirs(logFileDirectory)

        # Define log filename based on date
        logFilename = logFileDirectory+"DownloadRouterConfig_"+date+".log"

        # Check to see if logFilename currently exists.  If it does, append an
        # integer onto the end of the filename until logFilename no longer exists
        incrementLogFilename = 1
        while fileExist(logFilename):
            logFilename = logFileDirectory+"DownloadRouterConfig_"+date+"_"+str(incrementLogFilename)+".log"
            incrementLogFilename = incrementLogFilename + 1

        # Write log results to logFile
        with open(logFilename, "w") as outputLogFile:
            try:
                outputLogFile.write(summarize(logger))

            # Exception: router file was not able to be opened
            except IOError:
                print
                print "--> An error occurred opening "+logFileDirectory+logFile+"."

    else: # if fileExist(routerFile):
    # Else if no routerFile exists, create a sample one and quit the program.
        try:
            with open (routerFile, "w") as exampleFile:
                print
                print "--> Router file not found; Creating "+routerFile+"."
                print "    Edit this file and restart the application."
                exampleFile.write("## DownloadRouterConfig.py ROUTER FILE ##\n#\n")
                exampleFile.write("#Enter a list of hostnames or IP Addresses, one per line.\n#For example:\n")
                exampleFile.write("192.168.1.1\n192.168.1.2\nRouterA\nRouterB\nRouterC\netc...")
        
        # Exception: file could not be created
        except IOError:
            print
            print "--> Required file "+routerFile+" not found; An error has occurred creating "+routerFile+"."
            print "This file must contain a list, one per line, of Hostnames or IP addresses the"
            print "application will then connect to download the running-config."

print
print "--> Done."
raw_input() # Pause for user input.