from metactl import cli, config

class Context(object):
    def __init__(self):
        self.args = cli.parser.parse_args()
        self.app = self.args.APP
        self.config = config.parse_config(self.app)

def run():
    ctx = Context()
    ctx.args.func(ctx)
