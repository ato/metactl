metactl
=======

**Status:** Nothing to see here yet.

Metactl is an experimental next-generation version of a service lifecycle management script I wrote for work.

Features I want to keep from the original:

* Friendly CLI
* Good Java/Jetty integration
* SCM-based deployments
* Both Solaris and Linux support
* Integration with OS service manager (SMF, Upstart, Systemd)

Features under consideration for metactl:

* Support for other programming languages
* Multiple service entry points (multiple daemons, crontab)
* Distributed deployments (eg bump all production instances of myapp to version 1.2.3)
* Dynamic registration with a load balancer
* Configuration inheritance (per-app, per-site, per-server)
* Optional per-app IP and DNS addresses for debugging and discovery
* Lightweight sandboxing (using containers/zones)

Configuration
-------------

Metactl has four layers of configuration that are merged together for each instance.

### Application defaults

A per-app config file is checked into version control as `.metactl`. It is used for 
configuration common across all instances of an application such as entry points
and universal defaults.

```ini
[env]
JOB_MANAGER_PORT = 9000

[daemon.webapp]
platform = jetty6
jvm.heap.max = 256m

[daemon.jobmanager]
platform = jvm
jvm.jar = jobmanager.jar %(JOB_MANAGER_PORT)
jvm.heap.max = 128m

[crontab]
daily housekeeping = 5 0 * * * curl http://localhost/housekeeping
harvest data on mondays = 10 0 * * 1 java -jar harvest.jar
```

### Site configuration

Site configuration overrides app defaults for a particular deployment environment
(devel, test, production etc). It lives in some central location that's yet to be
decided.

```ini
[env]
DB_URL = mysql://myapp:secret@mysql-prod.example.org/myapp

[build]
repo = svn://svn.example.org/myapp
tag = 1.2.3
```

### Node configuration

Node configuration overrides site configuration for a particular deployed instance
of an app on a particular server. It lives in `/etc/metactl/nodes/myapp.conf` on
the individual server.

```ini
[env]
# change port because 9000 is already taken on this server
JOB_MANAGER_PORT = 9001
```

Implementation thoughts
-----------------------

### Language

I wrote the original tool in a combination of bash and Perl in order to support 
Solaris 9 easily. For metactl I'll instead set a baseline of Solaris 10 and RHEL 5. That 
gives us four choices: bash, C, Perl, Python.

Metactl is going to have more sophisticated configuration and coordination which will
be hard to maintain in bash. C would not be a bad choice but a managed language would
allow for rapid implementation and experimentation.  My current plan is to go with 
Python as it has good error handling and I'm more fluent in it than in Perl.

### Distributed coordination/configuration

I'm tempted to use [Zookeeper](https://zookeeper.apache.org/) since we're going to
be running it anyway for Solr, a relatively simple model, no single point of failure 
and bindings for most languages.

Another option is [Mcollective](https://puppetlabs.com/mcollective/introduction/).

### Linux Containers

Something I've wanted to explore for a while now is a simple sandboxing mechanism to
manage resources, prevent applications from having surprise dependencies on shared
filesystems and to limit damage in the event of a break in. Other attempts to achieve
this I've seen are to use a one-app-per-VM model or SELinux. One-app-per-VM is resource
wasteful and makes system administration harder. SELinux is just notoriously complicated.

#### Network namespaces

Let's start off by running bash in a new network namespace using `unshare`.  Notice how 
all the network interfaces disappear:

    xterm1 / $ ip addr
    # ip addr
    1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN 
        link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
        inet 127.0.0.1/8 scope host lo
    2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP qlen 1000
        link/ether 12:34:45:67:89:01 brd ff:ff:ff:ff:ff:ff
        inet 192.168.0.1/24 brd 192.168.0.255 scope global eth0
    xterm1 / $ unshare --net bash
    xterm1 / $ ip addr
    1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN 
        link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
        inet 127.0.0.1/8 scope host lo
    xterm1 / $ echo $$
    24749

In another terminal (which is still in the parent namespace) let's create a virtual ethernet
link between the parent and child. We'll name the parent's end of the link pid24749 so we know
which process it's linked to.  We'll also add a static route for 192.168.0.5 which will be
the child's IP address.

    xterm2 / $ ip link add pid24749 type veth peer name veth0 netns 24749
    xterm2 / $ ip link set pid24749 up
    xterm2 / $ ip route add 192.168.0.5/32 dev pid24749
    xterm2 / $ ip addr
    1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN 
        link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
        inet 127.0.0.1/8 scope host lo
    2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP qlen 1000
        link/ether 12:34:45:67:89:01 brd ff:ff:ff:ff:ff:ff
        inet 192.168.0.1/24 brd 192.168.0.255 scope global eth0
    3: pid24749: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc pfifo_fast state DOWN qlen 1000
        link/ether ea:d7:39:fb:e1:b4 brd ff:ff:ff:ff:ff:ff

Now let's configure the child's end of the link:

    xterm1 / $ ip link set veth0 up
    xterm1 / $ ip addr add 192.168.0.5/32 dev veth0
    xterm1 / $ ip route add default dev veth0
    xterm1 / $ ip addr
    1: lo: <LOOPBACK> mtu 65536 qdisc noop state DOWN 
        link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    2: veth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP qlen 1000
        link/ether 66:39:e6:bb:02:c3 brd ff:ff:ff:ff:ff:ff
        inet 192.168.0.5/32 scope global veth0
    xterm1 / $ ping 192.168.0.1
    PING 192.168.0.1 (192.168.0.1) 56(84) bytes of data.
    64 bytes from 192.168.0.1: icmp_seq=1 ttl=64 time=0.122 ms
    64 bytes from 192.168.0.1: icmp_seq=2 ttl=64 time=0.113 ms
    ...
