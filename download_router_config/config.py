"""Download Router Config."""

import os

# Application Variables
app_dict = {
    "author": "Aaron Melton <aaron.melton@fiserv.com>",
    "date": "2022-01-12",
    "desc": "A Python script to capture the running-config of Cisco routers and switches",
    "name": "download_router_config.py",
    "title": "Download Router Config",
    "url": "https://github.com/aaronmelton/DownloadRouterConfig",
    "version": "3.0.0",
}

# Logging Variables
log_dict = {
    "level": os.environ.get("LOG_LEVEL"),
    "path": os.environ.get("LOG_PATH"),
    "prefix": os.environ.get("LOG_PREFIX"),
}
