"""download-router-config."""
# !/usr/bin/env python
# -*- coding: utf-8 -*-
#

import sys
from datetime import datetime
from os import getcwd
from time import perf_counter

from aaron_common_libs.common_funcs import argument, cli, subcommand
from aaron_common_libs.logger.custom_logger import CustomLogger
from config import Config
from napalm import get_network_driver
from napalm.base.exceptions import ConnectionException
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TimeElapsedColumn
from rich.prompt import Prompt

console = Console()
config = Config()
logging_handler = CustomLogger(log_dict=config.log_dict)
logger = logging_handler.default
logger_all = logging_handler.all


# Sub-Commands for Download operations
@subcommand(
    [
        argument(
            "--device_list",
            help="Text file containing Cisco device Hostnames or IP Addresses.",
            type=str,
            nargs=1,
            required=False,
        ),
        argument("--backup_to", help="Path to save config files to.", type=str, nargs=1, required=False),
    ]
)
def download(args):
    """Subcommand options for download operations."""
    logger.debug("args==%s", vars(args))

    console.rule(f"""{config.app_dict["title"]} {config.app_dict["version"]} ({config.app_dict["date"]})""")

    if not args.backup_to:
        backup_to = f"{getcwd()}/"
    else:
        backup_to = args.backup_to[0]
        if backup_to[-1] != "/":
            backup_to += "/"
    if args.device_list and backup_to:
        console.print(f"""[green]-->[/green] Attempting to open file '{args.device_list[0]}'...""")

        with open(args.device_list[0], "r", encoding="utf-8") as input_file:
            logger.info("Reading contents of '%s'...", args.device_list[0])
            console.print(f""" [green]->[/green] Reading contents of '{args.device_list[0]}'...""")
            device_list = input_file.read().splitlines()

        logger.info("%s devices read from '%s'", len(device_list), args.device_list[0])
        console.print(f"""    {len(device_list)} devices read from '{args.device_list[0]}'""")
        print("")
        get_username = Prompt.ask("Username", default="cisco")
        get_password = Prompt.ask("Password", password=True)
        print("")

        counters = {"success": 0, "fail": 0}

        with open(
            f"""{backup_to}download_router_config_summary_{datetime.now().strftime("%Y%m%dT%H%M%S")}.csv""",
            "w",
            encoding="utf-8",
        ) as summary_csv:
            with Progress(
                SpinnerColumn(),
                *Progress.get_default_columns(),
                TimeElapsedColumn(),
                console=console,
                transient=False,
            ) as progress_bar:
                download_configs = progress_bar.add_task("[red]Downloading...", total=len(device_list))
                for device in device_list:
                    try:
                        logger.debug("Connecting to device '%s'...", device)
                        napalm_driver = get_network_driver("ios")
                        connect_device = napalm_driver(
                            **{
                                "hostname": device,
                                "username": get_username,
                                "password": get_password,
                            }
                        )
                        connect_device.open()
                        summary_csv.write(f"{device},success\n")
                        with open(
                            f"""{backup_to}{device}_config_{datetime.now().strftime("%Y%m%dT%H%M%S")}.log""",
                            "w",
                            encoding="utf-8",
                        ) as config_backup:
                            config_backup.write(connect_device.get_config()["running"])
                        connect_device.close()
                        counters["success"] += 1
                    except ConnectionException as some_exception:
                        logger.warning("ERROR==%s", some_exception)
                        console.print(f"""[bright_yellow]WARNING:[/bright_yellow] {some_exception}""")
                        summary_csv.write(f"{device},fail\n")
                        counters["fail"] += 1
                    progress_bar.advance(download_configs)

        logger.info("[%s/%s] devices successfully backed up.", counters["success"], len(device_list))
        logger.info("[%s/%s] devices failed to back up.", counters["fail"], len(device_list))
        console.rule("Summary")
        if counters["success"]:
            console.print(f"""[{counters["success"]}/{len(device_list)}] successfully backed up.""")
        if counters["fail"]:
            console.print(f"""[{counters["fail"]}/{len(device_list)}] failed to back up.""")


def main():
    """Do Something.

    Args
    ----

    Returns
    -------
    None
    """
    start_time = perf_counter()

    logger.info("")
    logger_all.info("---------- START START START ----------")
    logger_all.info(
        "%s v%s (%s)",
        config.app_dict["title"],
        config.app_dict["version"],
        config.app_dict["date"],
    )

    args = cli.parse_args()
    if args.subcommand is None:
        cli.print_help()
    else:
        args.func(args)

    logger_all.info("Total Execution Time: %s seconds", round(perf_counter() - start_time, 2))
    logger_all.info("----------   STOP STOP STOP  ----------")
    logger.info("")


if __name__ == "__main__":
    sys.exit(main())
