from os.path import abspath, dirname
from YamJam import yamjam

config = yamjam()['reapy']

BASE_DIR = dirname(dirname(abspath(__file__)))

USER = config['user']

DEFAULT_DSN = config['default-dsn']

TESTING_DSN = config['testing-dsn']
