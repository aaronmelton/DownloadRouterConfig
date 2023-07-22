# CHANGELOG

## [3.1.0] - 2023-07-22
### Changed
- Simplified script by moving config.py into the script file as a dataclass.
- Updating Python libraries.


## [3.0.3] - 2022-07-05
### Changed
- Improving functionality that times app from using time.time() to 
  time.perf_counter().
- Updating cffi (1.15.0 -> 1.15.1)
- Updating bcrypt (3.2.0 -> 3.2.2)
- Updating cryptography (36.0.1 -> 37.0.4)
- Updating lxml (4.8.0 -> 4.9.1)
- Updating markupsafe (2.1.0 -> 2.1.1)
- Updating paramiko (2.9.2 -> 2.11.0)
- Updating certifi (2021.10.8 -> 2022.6.15)
- Updating charset-normalizer (2.0.12 -> 2.1.0)
- Updating dnspython (2.2.0 -> 2.2.1)
- Updating jinja2 (3.0.3 -> 3.1.2)
- Updating ncclient (0.6.9 -> 0.6.13)
- Updating pbr (5.8.1 -> 5.9.0)
- Updating pyparsing (3.0.7 -> 3.0.9)
- Updating urllib3 (1.26.8 -> 1.26.9)
- Updating wrapt (1.13.3 -> 1.14.1)
- Updating astroid (2.9.3 -> 2.11.6)
- Updating ciscoconfparse (1.6.36 -> 1.6.40)
- Updating click (8.0.4 -> 8.1.3)
- Installing dill (0.3.5.1)
- Updating junos-eznc (2.6.3 -> 2.6.4)
- Updating platformdirs (2.5.1 -> 2.5.2)
- Updating requests (2.27.1 -> 2.28.1)
- Installing tomlkit (0.11.0)
- Updating bandit (1.7.3 -> 1.7.4)
- Updating black (22.1.0 -> 22.6.0)
- Updating napalm (3.3.1 -> 3.4.1)
- Updating pylint (2.12.2 -> 2.14.4)
- Updating pytest (7.0.1 -> 7.1.2)


## [3.0.2] - 2022-02-07
### Added
- Dockerfile
### Changed
- README.md: Added instructions for using the script with Docker.
- download_router_config.py: Removed superfluous logging lines.
- pyproject.toml: Moved development-only packages into [tool.poetry.dev-dependencies]
- TODO.md: Dealt with Pylint issues.
### Removed
- __init__.py: Not necessary.

## [3.0.1] - 2022-01-14
### Added
- pyproject.toml: Moving in bandit, black, pytdocstyle, pylint configuration
  options.
- pyproject.toml: Added pytest.
- Added isort package.
### Changed
- README.md: Cleaning up text.
- Removed pylint comments from code.
- Gave summary log file an appropriate variable name, like 'summary_csv' and not
  'something'.
### Removed
- .bandit.yml; Moved into pyproject.toml
- .pydocstyle.ini; Moved into pyproject.toml
- .yamllint; Not using any YAML in this project.

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