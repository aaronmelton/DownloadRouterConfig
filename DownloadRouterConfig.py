#!/usr/bin/python
#
# DownloadRouterConfig.py
# Copyright (C) 2012-2013 Aaron Melton <aaron(at)aaronmelton(dot)com>
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


import datetime	# Required for date format
import Exscript	# Required for SSH, queue & logging functionality
import os		# Required to determine OS of host

from Exscript                   import Queue, Host, Logger
from Exscript.protocols 		import SSH2
from Exscript.util.file			import get_hosts_from_file
from Exscript.util.log          import log_to
from Exscript.util.decorator    import autologin
from Exscript.util.interact     import read_login
from Exscript.util.report		import status,summarize

logger = Logger()	# Log stuff
@log_to(logger)	# Logging descriptor
@autologin()	# Exscript login descriptor

def downloadRouterConfig(job, host, socket):
	socket.execute('terminal length 0')	# Disable user-prompt to page through config
										# Exscript doesn't always recognize Cisco IOS
										# for socket.autoinit() to work correctly
	socket.execute('show run')	# Show running config

	configDirectory = ('configs_'+date+'/')	# Define directory to hold config files
	if not os.path.exists(configDirectory): os.mkdir(configDirectory) # Create config file directory if it doesn't exist
		
	outputFileName = host.get_name()+'_Config_'+date+'.txt'	# Define output filename based on hostname and date
	outputFile = file(configDirectory+outputFileName,'w')	# Open output file (will overwrite contents)

	outputFile.write(socket.response)	# Write contents of running config to output file
	outputFile.close()					# Close output file
	socket.send('exit\r')				# Send the "exit" command to log out of router gracefully
	socket.close()						# Close SSH connection

# Determine OS in use and clear screen of previous output
os.system('cls' if os.name=='nt' else 'clear')

print 'Download Router Configuration v2.14'
print '-----------------------------------'
print

try:	# Check for existance of 'routers.lst'; If exists, continue with program
	with open('routers.lst'): pass
	# Define 'date' variable for use in the output filename
	date = datetime.datetime.now()		# Determine today's date
	date = date.strftime('%Y-%m-%d')	# Format date as YYYY-MM-DD

	# Read hosts from specified file & remove duplicate entries, set protocol to SSH2
	hosts = get_hosts_from_file('routers.lst',default_protocol='ssh2',remove_duplicates=True)
	userCreds = read_login()	# Prompt the user for his name and password

	print # Required for pretty spacing. :)

	queue = Queue(verbose=1, max_threads=4)	# Minimal message from queue, 4 threads
	queue.add_account(userCreds)			# Use supplied user credentials
	queue.run(hosts, downloadRouterConfig)	# Create queue using provided hosts
	queue.shutdown()						# End all running threads and close queue

	print status(logger)	# Print current % status of operation to screen

	logFile = open('status_'+date+'.log', 'w')	# Open 'status.log' file
	logFile.write(summarize(logger))	# Write results of program to file
	logFile.close()						# Close 'status.log' file
	
except IOError:	# If 'routers.lst' does not exist, provide error and quit
	print 'File routers.lst does not exist!'
	print 'Please create a file named \'routers.lst\' and place it in the same directory'
	print 'as the script. This file must contain a list, one per line, of hostnames or IP'
	print 'addresses the application will then connect to download the running-config.'
