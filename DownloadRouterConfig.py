#!/usr/bin/python
#
# DownloadRouterConfig.py
# Copyright (C) 2012  Aaron Melton <aaron(at)aaronmelton(dot)com>
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


# Required Modules
import datetime					# Required for date format
import Exscript					# Required for SSH, queue & logging functionality
import os						# Required to determine OS of host

from Exscript                   import Queue, Host, Logger
from Exscript.protocols 		import SSH2
from Exscript.util.file			import get_hosts_from_file
from Exscript.util.log          import log_to
from Exscript.util.decorator    import autologin
from Exscript.util.interact     import read_login
from Exscript.util.report		import status,summarize

# Determine OS in use and clear screen of previous output
os.system('cls' if os.name=='nt' else 'clear')

print ('Download Router Configuration')
print ('-----------------------------')

# Define 'date' variable for use in the output filename
date = datetime.datetime.now()		# Determine today's date
date = date.strftime('%Y-%m-%d')	# Format date as YYYY-MM-DD

logger = Logger()	# Log stuff

@log_to(logger)
@autologin()
def downloadRouterConfig(job, host, socket):
    print 
    socket.execute('terminal length 0')							# Disable user-prompt to page through config
																# Exscript doesn't always recognize Cisco IOS
																# for socket.autoinit() to work correctly
	
    print '--> Extracting running-config from '+host.get_name()
	
    socket.execute('show run')									# Show running config
    outputFileName = host.get_name()+'_Config_'+date+'.txt'     # Define output filename based on hostname and date
    outputFile = file(outputFileName,'w')						# Open output file (will overwrite contents)
	
    print
    print '--> Writing running-config to '+outputFileName
	
    outputFile.write(socket.response)		# Write contents of running config to output file
    outputFile.close()						# Close output file
    socket.send('exit\r')					# Send the "exit" command to log out of router gracefully
    socket.close()							# Close SSH connection
    
	# Different editors interpret line breaks differently so the code below cleans
    # up the file output so that it looks the same no matter if you're using
    # Notepad, Notepad++ or whatever.
    rewriteOutputFile = open(outputFileName, 'r')	# Open output file (read only)
    contents = rewriteOutputFile.read()             # Read file contents into varaible
    rewriteOutputFile.close()                       # Close output file
    
    #print '--> Stripping duplicate line breaks...'
    new_contents = contents.replace('\r\n', '\n')	# Remove double-spaces
    rewriteOutputFile = open(outputFileName, 'w')   # Open output file
    #print '--> ReWriting running-config to '+outputFileName
    rewriteOutputFile.write(new_contents)           # Overwrite contents of original output file
    rewriteOutputFile.close()                       # Close output file
    print

hosts = get_hosts_from_file('routers.lst',default_protocol='ssh2',remove_duplicates=True)
userCreds = read_login()		# Prompt the user for his name and password

queue = Queue(verbose=1, max_threads=4)	# Minimal messages, 4 threads
queue.add_account(userCreds)			# Use supplied user credentials
queue.run(hosts, downloadRouterConfig)	# Create queue using provided hosts
queue.shutdown()						# End all running threads and close queue

print
print status(logger)	# Print current % status of operation to screen
print 

logFile = open('status.log', 'w')	# Open 'status.log' file
logFile.write(summarize(logger))	# Write results of program to file
logFile.close()						# Close 'status.log' file

print 
print 'Backup completed.'