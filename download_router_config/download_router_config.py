"""Download Router Config."""

import logging
import os
import sys
import time
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from dataclasses import dataclass
from datetime import date, datetime
from getpass import getpass

from napalm import get_network_driver
from progress.bar import Bar


@dataclass
class Config:
    """Class for Application variables."""

    def __init__(self):
        """Application Variables."""
        self.app_dict = {
            "author": "Aaron Melton <aaron@aaronmelton.com>",
            "date": "2023-07-22",
            "desc": "A Python script to capture the running-config of Cisco routers and switches.",
            "name": "download_router_config.py",
            "title": "Download Router Config",
            "url": "https://github.com/aaronmelton/DownloadRouterConfig",
            "version": "3.1.0",
        }

        # Logging Variables
        self.log_dict = {
            "level": os.environ.get("LOG_LEVEL", None),
            "path": os.environ.get("LOG_PATH", None),
            "prefix": "download_router_config_",
        }


config = Config()


def main():  # pylint: disable=broad-except,too-many-locals,too-many-statements
    """Main Function.

    Args
    ----
    args : dict

    Returns
    -------
    None
    """
    start_time = time.perf_counter()

    parser = ArgumentParser(
        formatter_class=RawDescriptionHelpFormatter,
        description=f"""{config.app_dict["name"]} {config.app_dict["version"]} {config.app_dict["date"]}\n--\nDescription: {config.app_dict["desc"]}\nAuthor:      {config.app_dict["author"]}\nURL:         {config.app_dict["url"]}""",
    )
    parser.add_argument(
        "--device_list",
        help="Text file containing Cisco device Hostnames or IP Addresses.",
        required=True,
    )
    parser.add_argument(
        "--backup_to",
        help="Directory to save config files.",
        required=False,
    )
    args = parser.parse_args()

    # Setup Logging Functionality
    logging.basicConfig(
        filename=f"""{config.log_dict["path"]}{config.log_dict["prefix"]}{date.today().strftime("%Y%m%d")}.log""",
        filemode="a",
        format="{asctime}  Log Level: {levelname:8}  Line: {lineno:4}  Function: {funcName:21}  Msg: {message}",
        style="{",
        datefmt="%Y-%m-%dT%H:%M:%S",
        level=config.log_dict["level"],
    )

    logger.debug("START START START")

    script_header = f"""{config.app_dict["title"]} {config.app_dict["version"]} ({config.app_dict["date"]})"""
    logger.info(script_header)
    logger.info("=" * len(script_header))

    if vars(args)["backup_to"]:
        ###
        # NEED TO VALIDATE DIRECTORY EXISTS
        ###
        backup_to = vars(args)["backup_to"]
    else:
        logger.warning("--> Backup directory not provided; Assuming current working directory.")
        backup_to = os.getcwd()

    logger.info(f"""--> Attempting to open file '{vars(args)["device_list"]}'...""")
    with open(vars(args)["device_list"], "r", encoding="utf-8") as input_file:
        logger.info(f"""--> Reading contents of '{vars(args)["device_list"]}'...""")
        device_list = input_file.read().splitlines()

    logger.info(f"""--> Read [{len(device_list)}] devices from '{vars(args)["device_list"]}'.""")
    logger.info("")

    get_username = input("Username: ")
    get_password = getpass("Password: ")
    logger.info("")
    success_count = 0
    fail_count = 0

    summary_filename = f"""download_router_config_summary_{datetime.now().strftime("%Y%m%dT%H%M%S")}.csv"""
    with open(f"{backup_to}{summary_filename}", "w", encoding="utf-8") as summary_csv:
        for device in Bar("Working...", suffix="%(percent).f%% - %(eta)ds").iter(device_list):
            device_dict = {
                "hostname": device,
                "username": get_username,
                "password": get_password,
            }
            connect_device = None
            try:
                napalm_driver = get_network_driver("ios")
                connect_device = napalm_driver(**device_dict)
                connect_device.open()
                summary_csv.write(f"{device},success\n")
                device_filename = f"""{device}_config_{datetime.now().strftime("%Y%m%dT%H%M%S")}.log"""
                with open(f"{backup_to}{device_filename}", "w", encoding="utf-8") as config_backup:
                    config_backup.write(connect_device.get_config()["running"])
                connect_device.close()
                success_count += 1
            except Exception:  # pylint: disable=broad-except
                summary_csv.write(f"{device},fail\n")
                fail_count += 1

    logger.info("")
    logger.info("Backup Summary:")
    logger.info(f"""Device backup successful: {success_count}""")
    logger.info(f"""Device backup failed:     {fail_count}""")
    logger.info("")
    logger.info(f"Total Execution Time: {(time.perf_counter() - start_time):.2f} seconds")
    logger.debug("STOP STOP STOP")
    return 0


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    log_to_console = logging.StreamHandler()
    log_to_console.setLevel(logging.INFO)
    logger.addHandler(log_to_console)
    sys.exit(main())
