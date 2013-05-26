import os, sys
from metactl import cli, config

def config_editor(ctx):
    editor = os.environ.get('EDITOR', 'vi')
    os.execvp(editor, [editor, config.local_file(ctx.app)])

parser = cli.subparsers.add_parser('config', help='open config file in $EDITOR')
parser.set_defaults(func=config_editor)

def config_show(ctx):
    ctx.config.write(sys.stdout)

parser = cli.subparsers.add_parser('show', help='print configuration')
parser.set_defaults(func=config_show)
