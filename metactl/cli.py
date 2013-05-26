import argparse
from metactl.config import parse_config

parser = argparse.ArgumentParser()
parser.add_argument('APP', help='application name')
subparsers = parser.add_subparsers(help='sub-command help')

class Context(object):
    def __init__(self):
        self.args = parser.parse_args()
        self.app = self.args.APP
        self.config = parse_config(self.app)

def main():
    ctx = Context()
    ctx.args.func(ctx)
