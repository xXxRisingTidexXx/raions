"""
This module provides some basic constants

Generally, the main global constants are collected here.
"""
import YamJam
from os.path import abspath, dirname

# Basic YAML configuration located at ~/.yamjam/config.yaml
config = YamJam.yamjam()['reapy']

# Project's root folder
BASE_DIR = dirname(dirname(abspath(__file__)))

# Python interpreter's path needed by cron schedule
INTERPRETER_PATH = config['interpreter-path']

# Linux user who launches the cron schedule
USER = config['user']

# Main PostgreSQL database's url
DEFAULT_DSN = config['default-dsn']

# Testing PostgreSQL database's url
TESTING_DSN = config['testing-dsn']
