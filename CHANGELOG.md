# CHANGELOG

## [3.0.0] - 2022-01-11
### Changed
- Porting code from Python2 to Python3!


## DownloadRouterConfig.py v2.2.3 (2014-03-17) ##
* Replaced tab with four spaces.
* Corrected variables in code accidentally copied from another application.
* Changed 'BackupStatus' log filename to 'DownloadRouterConfig'.
* Replaced ' with " to be consistent throughout the file.
* Updated `README.md` to match newest application design.
* Corrected problem where application would fail if logFileDirectory or 
  backupFileDirectory in settings.cfg was blank.

## DownloadRouterConfig.py v2.2.2 (2013-09-09) ##
* Corrected makedirs() functionality: Directories with a trailing backslash
  in the config file were not being created thereby causing the application
  to fail.
* Moved logFileDirectory & backupDirectory makedirs() function such that the
  directory would only be created if/when the parent function was called
  instead of creating both directories whenever the application executed.
* Removing example file since it's no longer up-to-date.

## DownloadRouterConfig.py v2.2.1 (2013-08-29) ##
* Corrected minor issue with Queue() function in which the verbose and 
  max_threads settings were not being correctly read from configFile.
* Improved log file output so that it no longer overwrites any existing
  files (incrementing integer at end of filename).
* Corrected 'mkdir' function to 'makedirs' so that directories will be
  created recursively, if they do not exist.
* Suppressed error SPAM from stdout by adding stderr=(open(os.devnull, 'w'))
  to the Queue() function. (Errors are still written to the log.)
  
## DownloadRouterConfig.py v2.2.0 (2013-08-22) ##
* Added configFile functionality to give application the ability to retrieve
  user-specified settings from a config file.  Application use now extended
  such that the list of routers, index and respective paths can be specified
  in the file.  Application can also use configured username and password.

## DownloadRouterConfig.py v2.1.18 (2013-08-15) ##
* Cleaned up module importing

## DownloadRouterConfig.py v2.1.17 (2013-07-29) ##
* Updating project to use Semantic Versioning: http://semver.org/
  Previous project versions were described using a MAJOR.PATCH increment
  instead of MAJOR.MINOR.PATCH increment.  In other words, adjusting the
  previous version 2.17 -- it's correct Semantic Version would be 2.1.17.

## DownloadRouterConfig.py 2.17 (2013-07-20) ##
* Making application a bit more extendible through the use of functions and
  variables.
* Improved file error handling.

## DownloadRouterConfig.py 2.16 (2013-07-18) ##
* Changed application to search for 'routers.txt' file instead of 'routers.lst'
  because some users were complaining about '.lst' not being a registered file
  extension in Windows. (Their user permissions did not allow them to associate
  this extension with Notepad, etc.)
* Changed the IOError function so that it would actually create a 'routers.txt'
  file should one be missing.  I felt this might be a better way to handle the
  situation should someone acquire the binary of this application without any
  supporting documentation to describe missing required files.

## DownloadRouterConfig.py 2.15 (2013-07-10) ##
* Updated the file open operation to specify opening the routers.lst file
  as read only.
* Minor corrections to the IOError message.

## DownloadRouterConfig.py 2.14 (2013-04-16) ##
* Determined there was no bug with the queuing function; I was passing
  the program a very large list of hosts that contained duplicate
  hostnames that I thought I had removed.  The function removed all
  these duplicates resulting in a number lower than I was expecting.
* Changing date string from 'YYYY-MM-DD' to 'YYYYMMDD' to match common
  filenames used in our environment.

## DownloadRouterConfig.py 2.14 (2013-04-12) ##
* Renamed 'logs' directory to 'configs' to be consistent with what
  the application is actually doing. (It's not downloading logs.)
* Added date to the 'status.log' file for easier identification and to
  prevent the file being recently overwritten.  May eventually change
  date to be a timestamp instead?

## DownloadRouterConfig.py 2.14 (2013-04-11) ##
* Added error checking for 'routers.lst' file.
* Added ability for application to save log files to a subdirectory.

## DownloadRouterConfig.py 2.13 (2013-04-10) ##
* Updated CHANGELOG: New version
* Updated README: Cleaned up some text
* Updated TODO: Changed format a bit, checked off item
* Moved some code around just to tidy things up (functionality not changed).
* Removed unimportant debugging information from the code that displayed
  current operation as the logging capabilities of the queue are informative
  enough.
* Removed the 'rewriteOutputFile' operation because testing showed that
  Notepad** (the default editor I use in Windows) is the only application
  that displays duplicate blank lines whereas other text editors do not.

## DownloadRouterConfig.py 2.12 (2013-04-08) ##
* Added LICENSE information to source code.
* Removed company-specific information from code.
* Initial source code commit to GitHub

(specific details of what changed between v2.0 and v2.11 not captured)

## DownloadRouterConfig.py 2.0 (2012-03-26) ##
* Added logging functionality to keep track of which routers' configurations
  were downloaded and the specific error code for those that were not.

----------
(specific details of what changed between v1.0 and v2.0 not captured)

----------

## DownloadRouterConfig.py 1.0 (2012-11-02) ##
* Initial "release" of application built on Exscript. Includes only the most
  basic functionality used to download router configs.