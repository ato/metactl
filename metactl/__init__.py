# general commands
import metactl.edit
import metactl.daemon

# platform-specific commands
import platform
if platform.system() == 'Linux':
    import metactl.netns
