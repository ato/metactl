# general commands
import metactl.edit
import metactl.daemon
import metactl.container

# platform-specific commands
import platform
if platform.system() == 'Linux':
    import metactl.netns
