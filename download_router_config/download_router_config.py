"""Download Router Config."""

import argparse
import datetime
import getpass
import logging
import os
import sys
import time
import napalm
from progress.bar import Bar

import config


def main():
    """Main Function.

    Args
    ----
    args : dict

    Returns
    -------
    None
    """
    start_time = time.time()

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        # pylint: disable=line-too-long
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
        # pylint: disable=line-too-long
        filename=f"""{config.log_dict["path"]}{config.log_dict["prefix"]}{datetime.date.today().strftime("%Y%m%d")}.log""",
        filemode="a",
        format="{asctime}  Log Level: {levelname:8}  Line: {lineno:4}  Function: {funcName:21}  Msg: {message}",
        style="{",
        datefmt="%Y-%m-%dT%H:%M:%S",
        level=config.log_dict["level"],
    )

    logger.debug("")
    logger.debug("")
    logger.debug("")
    logger.debug("START START START")

    # pylint: disable=line-too-long
    script_header = f"""{config.app_dict["title"]} {config.app_dict["version"]} ({config.app_dict["date"]})"""
    logger.info(script_header)
    logger.info("=" * len(script_header))

    if vars(args)["backup_to"]:
        backup_to = vars(args)["backup_to"]
    else:
        logger.warning(
            "--> Backup directory not provided; Assuming current working directory."
        )
        backup_to = os.getcwd()

    logger.info(f"""--> Attempting to open file '{vars(args)["device_list"]}'...""")
    with open(vars(args)["device_list"], "r", encoding="utf-8") as input_file:
        logger.info(f"""--> Reading contents of '{vars(args)["device_list"]}'...""")
        device_list = input_file.read().splitlines()

    logger.info(
        f"""--> Read [{len(device_list)}] devices from '{vars(args)["device_list"]}'."""
    )
    logger.info("")

    get_username = input("Username: ")
    get_password = getpass.getpass("Password: ")
    logger.info("")
    success_count = 0
    fail_count = 0

    with open("something.log", "w", encoding="utf-8") as something:
        for device in Bar("Working...", suffix="%(percent).f%% - %(eta)ds").iter(
            device_list
        ):
            device_dict = {
                "hostname": device,
                "username": get_username,
                "password": get_password,
            }
            connect_device = None
            try:
                driver = napalm.get_network_driver("ios")
                connect_device = driver(**device_dict)
                connect_device.open()
                something.write(f"{device},success\n")
                # pylint: disable=line-too-long
                device_filename = f"""{device}_config_{datetime.datetime.now().strftime("%Y%m%dT%H%M%S")}.log"""
                with open(
                    f"{backup_to}{device_filename}", "w", encoding="utf-8"
                ) as config_backup:
                    config_backup.write(connect_device.get_config()["running"])
                connect_device.close()
                success_count += 1
            except Exception:
                something.write(f"{device},fail\n")
                fail_count += 1

    logger.info("")
    logger.info("Backup Summary:")
    logger.info(f"""Device backup successful: {success_count}""")
    logger.info(f"""Device backup failed:     {fail_count}""")
    logger.info("")
    logger.info(f"Total Execution Time: {(time.time() - start_time):.2f} seconds")
    logger.debug("STOP STOP STOP")
    return 0


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    log_to_console = logging.StreamHandler()
    log_to_console.setLevel(logging.INFO)
    logger.addHandler(log_to_console)
    sys.exit(main())
