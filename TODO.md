# DownloadRouterConfig.py #

----------


## Needs Fixing ##
- [X] Queue function seems to cap out at 4,573 hosts? Fixed: User error.

## New Features ##
- [ ] Move application variables to a config file?
- [ ] Error checking: Enable access upon login?
- [X] Error checking: `routers.lst` exist?
- [X] Tidy up the application root directory by automatically creating a subdirectory to hold router configuration files.

## Nice To Have ##
- [ ] Adding a description of common errors encountered (as defined by and recorded by the Exscript module)?
- [X] Separate the `rewriteOutputFile` operations into their own function to prevent any possible interruption/delays in downloading config files.