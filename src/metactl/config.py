import ConfigParser, os

processors = []

def local_file(app):
    "Returns the path of the local config file."
    return '/tmp/' + app + '.conf'

def parse_config(app):
    config = ConfigParser.SafeConfigParser()
    config.read(local_file(app))
    for processor in processors:
        processor(config)
    return config
