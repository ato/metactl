import os, signal, ctypes, argparse, textwrap
from subprocess import check_call, Popen
from metactl import cli
from distutils.spawn import find_executable

CLONE_NEWNS = 0x00020000
CLONE_NEWNET = 0x40000000

def unshare(flags):
    libc = ctypes.CDLL("libc.so.6", use_errno=True)
    if libc.unshare(ctypes.c_int(flags)):
        errno = ctypes.get_errno()
        raise OSError(errno, os.strerror(errno))

def ip_veth_add(dev, netns):
    check_call(["ip", "link", "add", dev, "type", "veth", 
                "peer", "veth0", "netns", str(netns)])

def ip_route_add(dev, route):
    check_call(["ip", "route", "add", route, "dev", dev])

def ip_addr_add(dev, addr):
    check_call(["ip", "addr", "add", addr, "dev", dev])

def ip_link_up(dev):
    check_call(["ip", "link", "set", "dev", dev, "up"])

def wait_for_sigusr1():
    signal.signal(signal.SIGUSR1, lambda x, y: None)
    signal.alarm(10)
    signal.pause()
    signal.alarm(0)

def setup_network_child():
    unshare(CLONE_NEWNET)
    # Wait for parent to setup veth device
    wait_for_sigusr1()
    ip_link_up('lo')
    ip_link_up('veth0')
    ip_addr_add('veth0', '192.168.0.1/32')
    ip_route_add('veth0', 'default')

def setup_network_parent(child_pid):
    veth = "pid" + str(child_pid)
    ip_veth_add(veth, child_pid)
    ip_link_up(veth)
    ip_route_add(veth, '192.168.0.1/32')        
    os.kill(child_pid, signal.SIGUSR1)

if find_executable('tcpdump'):
    def tcpdump(ctx):
        os.execvp('tcpdump',['tcpdump'] + ctx.args.args)
    parser = cli.subparsers.add_parser(
        'tcpdump', prefix_chars='+',
        help='dump network traffic',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
        Captures network traffic to and from this application using tcpdump.
        Only available when network sandboxing is enabled and is equivalent to

           metactl myapp shell tcpdump -i veth0
        '''))
    parser.add_argument('args', nargs='*', help='arguments passed to tcpdump')
    parser.set_defaults(func=tcpdump)
