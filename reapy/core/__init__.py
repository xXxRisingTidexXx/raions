"""
This module provides some basic constants

Generally, the main global constants are collected here.
"""
from YamJam import yamjam
from os.path import abspath, dirname, join

# Project's root folder
BASE_DIR = dirname(dirname(abspath(__file__)))

# Basic YAML configuration located at ./.yamjam/config.yaml
config = yamjam(join(BASE_DIR, '.yamjam/config.yaml'))

# Linux user who launches the cron schedule
USER = config['user']

# Main PostgreSQL database's url
DEFAULT_DSN = config['default-dsn']

# Testing PostgreSQL database's url
TESTING_DSN = config['testing-dsn']
