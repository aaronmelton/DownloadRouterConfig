"""Test class Config."""
# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
# pylint: disable=invalid-name, duplicate-code

from re import match as re_match

from download_router_config.config import Config


def test_config():
    """Test config.py"""
    # Application Variables
    config = Config()
    assert config.app_dict["author"] == "Aaron Melton <aaron@aaronmelton.com>"
    assert re_match("\\d{4}(-\\d{2}){2}", "2023-12-27")
    assert config.app_dict["desc"] == "A Python script to capture the running-config of Cisco Routers and Switches."
    assert config.app_dict["title"] == "download_router_config"
    assert config.app_dict["url"] == "https://github.com/aaronmelton/DownloadRouterConfig"
    assert re_match("\\d{1,2}(\\.\\d{1,2}){2}", config.app_dict["version"])
