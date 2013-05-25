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

For each application Metactl has four layers of configuration:

* app defaults
* site defaults
* per instance

The application defaults are checked into version control in a top-level file `.metactl`. They
are used for configuration common across all instances of an application such as entry points
and defaults.

```ini
# .metactl - application defaults

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

