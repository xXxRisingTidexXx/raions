import YamJam
from os.path import abspath, dirname

config = YamJam.yamjam()['reapy']

BASE_DIR = dirname(dirname(abspath(__file__)))

INTERPRETER_PATH = config['interpreter-path']

USER = config['user']

DEFAULT_DSN = config['default-dsn']

TESTING_DSN = config['testing-dsn']
