import ConfigParser, os

def local_file(app):
    "Returns the path of the local config file."
    return '/tmp/' + app + '.conf'

def parse_config(app):
    p = ConfigParser.SafeConfigParser()
    p.read(local_file(app))
    return p
