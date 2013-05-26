import os
from configparser import ConfigParser, ExtendedInterpolation

processors = []

def local_file(app):
    "Returns the path of the local config file."
    return '/tmp/' + app + '.conf'

def parse_config(app):
    config = ConfigParser(interpolation=ExtendedInterpolation())
    config.read(local_file(app))
    for processor in processors:
        processor(config)
    return config
