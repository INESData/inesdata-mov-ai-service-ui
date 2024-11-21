# -*- coding: utf-8 -*-
"""This file sets the absolute path to the configuration file for the logger."""

from pathlib import Path

from .. import BASE_DIR

CONFIG_LOG = BASE_DIR.joinpath(Path("config/log.conf"))
