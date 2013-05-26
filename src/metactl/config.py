import os
import metactl
from configparser import ConfigParser, ExtendedInterpolation

def local_file(app):
    "Returns the path of the local config file."
    return '/tmp/' + app + '.conf'

def parse_config(app):
    config = ConfigParser(interpolation=ExtendedInterpolation(),
                          defaults=metactl.defaults)
    config.read(local_file(app))
    config.add_section('metactl')
    config['metactl']['app'] = app
    for processor in metactl.processors:
        processor(config)
    return config
