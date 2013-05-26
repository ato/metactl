import metactl.config

def java_options(config, section):
    options = []
    if config.has_option(section, 'java.heap.max'):
        options += ['-Xmx%(java.heap.max)']
    if config.has_option(section, 'java.heap.min'):
        options += ['-Xms%(java.heap.min)']
    config.set(section, 'java.options')

def java_home(section):
    if 'java.java' not in section:
        if 'java.home' in section:
            section['java.java'] = '${java.home}/bin/java'
        else:
            section['java.java'] = 'java'

def java_command(section):
    command = ['${java.java}']
    if 'java.heap.max' in section:
        command += ['-Xmx' + '${java.heap.max}']
    if 'java.heap.min' in section:
        command += ['-Xms' + '${java.heap.min}']
    if 'java.classpath' in section:
        command += ['-cp', '${java.classpath}']
    if 'java.options' in section:
        command += ['${java.options}']
    if 'java.main' in section:
        command += ['${java.main}']
    if 'java.jar' in section:
        command += ['-jar', '${java.jar}']
    if 'java.arguments' in section:
        command += ['${java.arguments}']
    if 'java.command' not in section:
        section['java.command'] = ' '.join(command)
    if 'command' not in section:
        section['command'] = '${java.command}'

def java_section(section):
    java_home(section)
    java_command(section)

def java_config(config):
    for section in config.sections():
        if section.startswith('daemon.'):
            if config[section].get('container','none') == 'java':
                java_section(config[section])

metactl.config.processors.append(java_config)
