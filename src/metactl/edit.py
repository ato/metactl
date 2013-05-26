import os, sys
from metactl import cli, config
from configparser import ConfigParser

def config_editor(ctx):
    editor = os.environ.get('EDITOR', 'vi')
    os.execvp(editor, [editor, config.local_file(ctx.app)])

parser = cli.subparsers.add_parser('config', help='open config file in $EDITOR')
parser.set_defaults(func=config_editor)

def interpolate(c):
    "Return a new config parser with all the items interpolated"
    out = ConfigParser(interpolation=None)
    for section in c.sections():
        out.add_section(section)
        for key, value in c[section].iteritems():
            out[section][key] = value
    return out

def config_show(ctx):
    c = ctx.config
    if ctx.args.interpolate:
        c = interpolate(c)
    c.write(sys.stdout)

parser = cli.subparsers.add_parser('show', help='print configuration')
parser.set_defaults(func=config_show)
parser.add_argument('-i', '--interpolate', action='store_true',
                    help='perform ${section:option} interpolation before printing')
