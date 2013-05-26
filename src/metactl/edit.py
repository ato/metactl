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

def print_section(c, section):
    if ':' in section:
        section, item = section.split(':', 2)
        print (c.get(section,item,raw=True))
    else:
        for item, value in c.items(section, raw=True):
            print item, '=', value

def show_config(ctx):
    c = ctx.config
    if ctx.args.interpolate:
        c = interpolate(c)
    if ctx.args.section:
        for section in ctx.args.section:
            print_section(c, section)
    else:
        c.write(sys.stdout)

parser = cli.subparsers.add_parser('show', help='print configuration')
parser.set_defaults(func=show_config)
parser.add_argument('-i', '--interpolate', action='store_true',
                    help='perform ${section:item} interpolation before printing')
parser.add_argument('section', nargs='*', help='print a particular section or section:item')
