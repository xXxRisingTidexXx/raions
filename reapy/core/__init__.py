"""
This module provides some basic constants

Generally, the main global constants are collected here.
"""
from YamJam import yamjam
from os.path import abspath, dirname

# Basic YAML configuration located at ~/.yamjam/config.yaml
CONFIG = yamjam()['reapy']

# Project's root folder
BASE_DIR = dirname(dirname(abspath(__file__)))

# Python interpreter's path needed by cron schedule
INTERPRETER_PATH = CONFIG['interpreter-path']

# Linux user who launches the cron schedule
USER = CONFIG['user']

# Main PostgreSQL database's url
DEFAULT_DSN = CONFIG['default-dsn']

# Testing PostgreSQL database's url
TESTING_DSN = CONFIG['testing-dsn']
