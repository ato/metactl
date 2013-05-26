import metactl.config

def jvm_options(config, section):
    options = []
    if config.has_option(section, 'jvm.heap.max'):
        options += ['-Xmx%(jvm.heap.max)']
    if config.has_option(section, 'jvm.heap.min'):
        options += ['-Xms%(jvm.heap.min)']
    config.set(section, 'jvm.options')

def jvm_command(config, section):
    command = []
    if config.has_option(section, 'jvm.options'):
        command += ['%(jvm.options)']    
    if config.has_option(section, 'jvm.classpath'):
        command += ['-cp', '%(jvm.classpath)']    
    if config.has_option(section, 'jvm.main'):
        command += ['%(jvm.main)']
    if config.has_option(section, 'jvm.jar'):
        command += ['-jar', '%(jvm.jar)']
    if not config.has_option(section, 'jvm.command'):
        config.set(section, 'jvm.command', ' '.join(command))

def jvm_section(config, section):
    jvm_command(config, section)

def jvm_config(config):
    for section in config.sections():
        if section.startswith('daemon.'):
            if config.has_option(section, 'container'):
                if config.get(section, 'container') == 'jvm':
                    jvm_section(config, section)
            
metactl.config.processors.append(jvm_config)
