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
