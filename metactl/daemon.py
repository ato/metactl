from metactl import cli, config
from subprocess import call

def run(ctx):
    call(ctx.config.get('daemon', 'command'), shell=True)

parser = cli.subparsers.add_parser('run', help='run the daemon command')
parser.set_defaults(func=run)

